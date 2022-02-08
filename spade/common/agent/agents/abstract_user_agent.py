import datetime
import logging
from abc import abstractmethod, ABC
from typing import List, Optional, Mapping

from spade.template import Template

from common.agent.agents.custom_metadata_fields import MasMessageMetadataFields
from common.agent.agents.my_abstract_agent import AbstractBaseAgent
from common.agent.behaviour.abstract_fsm_state_behaviours import AbstractWaitForChatMessageOrQuickReplyState
from common.agent.behaviour.behaviours import TrySubscriptionToAgentBehaviour, WaitForMessageFSMBehaviour
from common.agent.strategies.abstract_handling_strategies import AbstractHandlingStrategies
from common.chat.message.types import ChatMessage, ChatActualMessage
from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform, ChatAction
from common.chat.platform.factory import MessagingPlatformFactory
from common.chat.platform.types import ChatPlatform
from common.custom_chat.message_dao import AbstractMessageDAO
from common.database.user.abstract_user import AbstractBasicUser
from echo.common.database.user.daos import AbstractUnreadMessageDAO

logger = logging.getLogger(__name__)

MESSAGING_PLATFORM_API_TOKEN_METADATA_FIELD = 'messaging_platform_api_token'
"""The name of metadata field, which will contain the API token to communicate with the message origin platform"""


class AbstractUserAgent(AbstractBaseAgent, ABC):
    """An abstract base class for agents representing users"""

    def __init__(self, jid, password, user_id: str, gateway_agents_jids: List[str]):
        super().__init__(jid, password)

        self.user_id = user_id
        self.gateway_agents_jids = gateway_agents_jids

        self.user: Optional[AbstractBasicUser] = None
        self.messaging_platforms: Mapping[ChatPlatform, AbstractMessagingPlatform] = {}

    async def setup(self):
        await super().setup()

        for gateway_jid in self.gateway_agents_jids:
            msg_template = Template(to=self.jid_str)
            msg_template.metadata[MasMessageMetadataFields.SENDER.value] = gateway_jid
            self.add_behaviour(
                self.create_messaging_platform_receive_message_behaviour(),
                template=msg_template
            )
            self.add_behaviour(TrySubscriptionToAgentBehaviour(period=2, to_subscribe_agent_jid=gateway_jid))

        self.user = await self.retrieve_current_user()

    @abstractmethod
    def create_messaging_platform_receive_message_behaviour(self) -> WaitForMessageFSMBehaviour:
        """Template method to create the behaviour managing the messaging platform messages, coming from gateway"""
        pass

    async def refresh_current_user(self):
        self.user = await self.retrieve_current_user()

    @abstractmethod
    async def retrieve_current_user(self) -> AbstractBasicUser:
        """Template method to retrieve the represented user"""
        pass


class AbstractMessagingPlatformReceiveMessageState(AbstractWaitForChatMessageOrQuickReplyState, ABC):
    """The abstract FSM initial state in charge of managing messages coming from messaging platforms"""

    STATE_NAME = "AbstractMessagingPlatformReceiveMessageState"

    def __init__(self):
        super().__init__()

        self.user: Optional[AbstractBasicUser] = None
        self.messaging_platform: Optional[AbstractMessagingPlatform] = None
        self.messaging_platform_handling_strategies: Optional[AbstractHandlingStrategies] = None
        self.message_dao: Optional[AbstractMessageDAO] = None
        self.unread_message_dao: Optional[AbstractUnreadMessageDAO] = None

    async def on_start(self):
        await super().on_start()

        # Mirror agent field
        if self.user is None:
            self.user = self.agent.user

        if self.message_dao is None:
            self.message_dao = self.retrieve_message_dao()
            self.unread_message_dao = self.retrieve_unread_message_dao()

    async def refresh_user(self):
        await self.agent.refresh_current_user()
        self.user = self.agent.user

    async def before_handlers(self, mas_message, chat_message: ChatMessage) -> bool:

        agent_messaging_platforms: Mapping[ChatPlatform, AbstractMessagingPlatform] = self.agent.messaging_platforms

        # On message received retrieve the agent-stored messaging platform, if present
        current_message_agent_platform: Optional[AbstractMessagingPlatform] = (
            agent_messaging_platforms.get(chat_message.chat_platform, None)
        )
        if current_message_agent_platform:  # If agent has a messaging platform object, for current platform reuse it
            self.messaging_platform = current_message_agent_platform
        else:  # Otherwise, create my own platform and initialize even the agent one
            self.messaging_platform = MessagingPlatformFactory.platform_from(
                chat_message.chat_platform,
                mas_message.metadata[MESSAGING_PLATFORM_API_TOKEN_METADATA_FIELD],
                self.message_dao,
                self.unread_message_dao
            )
            self.agent.messaging_platforms[chat_message.chat_platform] = self.messaging_platform

        if self.should_show_typing_in_chat(chat_message):  # Show "typing..." in chat, if a message will follow
            await self.messaging_platform.send_chat_action(chat_message.sender_id, ChatAction.TYPING)

        # Initialize strategies on first message received
        self.messaging_platform_handling_strategies = self.create_platform_strategies(chat_message.chat_platform)
        # Performance: inefficient to recreate strategies for every interaction, use caching if platform doesn't change

        # Bind user chat platform id to its profile id
        self.messaging_platform_handling_strategies.bind_messaging_platform_id_to_user_id(self.user, chat_message)

        # Update user last interaction
        self.user.last_interaction = datetime.datetime.now()
        logger.info(f" Updated user last interaction, with the system, to: {str(self.user.last_interaction)}")

        return True  # Return true to continue handling the ongoing request

    async def handle_message(self, chat_actual_message: ChatActualMessage):
        if self.message_dao:
            # Save received user message if DAO present and the message is not of type 'upload'
            self.message_dao.insert(chat_actual_message.to_json())

    @abstractmethod
    def create_platform_strategies(self, chat_platform: ChatPlatform) -> AbstractHandlingStrategies:
        """Template method to create project and platform specific message handling strategies"""
        pass

    def retrieve_message_dao(self) -> Optional[AbstractMessageDAO]:
        """Returns the message dao for the messaging platform. Defaults returning None"""
        return None

    def retrieve_unread_message_dao(self) -> Optional[AbstractUnreadMessageDAO]:
        """Returns the unread message dao for the messaging platform. Defaults returning None"""
        return None

    def should_show_typing_in_chat(self, received_message: ChatMessage):
        """A property to tell if Typing chat action should be sent to the user, after receiving a message"""
        return not received_message.is_quick_reply
