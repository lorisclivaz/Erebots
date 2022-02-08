import logging
from abc import abstractmethod, ABC
from typing import Union, Optional

from spade.message import Message
from spade.template import Template

from common.agent.agents.abstract_gateway_agent import (
    AbstractGatewayAgent, CachedUser, AbstractAskForUserDataAboutMessageState, AbstractUserDataResponseHandlingState,
    UserAgentStartupHandler
)
from common.agent.agents.abstract_user_agent import MESSAGING_PLATFORM_API_TOKEN_METADATA_FIELD
from common.agent.agents.custom_metadata_fields import MasMessageMetadataFields, MasMessagePerformatives
from common.agent.agents.interaction_texts import localize
from common.agent.behaviour.behaviours import WaitForMessageFSMBehaviour
from common.agent.my_logging import log
from common.agent.presence_utils import find_contact_by_partial_name
from common.agent.utils import compose_user_agent_jid
from common.chat.message.types import ChatMessage
from common.chat.platform.abstract_messaging_platform import ChatAction
from covid19.common.agent.agents.interaction_texts import (
    NEW_USER_MESSAGE_NOT_LOCALIZED
)
from covid19.common.agent.agents.user.agent import UserAgent
from covid19.common.bootstrap_agent_names import ALL_PLATFORMS_GATEWAY_AGENTS_JIDS
from covid19.common.database.connection_manager import AbstractCovid19ConnectionManager
from covid19.common.database.user.factory import UserFactory

logger = logging.getLogger(__name__)


class AbstractCovid19GatewayAgent(AbstractGatewayAgent):
    """Abstract gateway agent for Covid19 project"""

    def __init__(self, jid, password, messaging_platform_sender_name: str, messaging_platform_api_token: str,
                 db_connection_manager: AbstractCovid19ConnectionManager):
        super().__init__(jid, password)

        self.messaging_platform_sender: str = messaging_platform_sender_name
        self.messaging_platform_api_token: str = messaging_platform_api_token
        self.db_connection_manager = db_connection_manager

    class AbstractCheckUserRegistrationState(AbstractAskForUserDataAboutMessageState, ABC):
        """A FSM behaviour state to handle the check for user registration to the system"""

        STATE_NAME = "AbstractCheckUserRegistrationState"

        def __init__(self, messaging_platform_api_token: str):
            super().__init__(messaging_platform_api_token, CHECK_REGISTRATION_CONTACT_PARTIAL_NAME)

        async def handle_already_cached_user(self, mas_message: Message, chat_message: ChatMessage,
                                             cached_user: CachedUser):
            doctor_jid = find_contact_by_partial_name(CHECK_REGISTRATION_CONTACT_PARTIAL_NAME, self.presence)
            await forward_message_to_user_agent(self, cached_user, mas_message, chat_message, doctor_jid)

        def create_response_handling_behaviour(self) -> WaitForMessageFSMBehaviour:
            class HandleUserRegistrationResponse(WaitForMessageFSMBehaviour):
                pass  # Only to change the class name shown in logging

            return HandleUserRegistrationResponse(
                lambda: self.agent.create_handle_user_registration_response_state(
                    self.agent.messaging_platform_api_token
                )
            )

    class AbstractHandleUserRegistrationResponseState(AbstractUserDataResponseHandlingState, ABC):
        """A FSM behaviour state to handle user registration status, coming back from DoctorAgent"""

        STATE_NAME = "AbstractHandleUserRegistrationResponseState"

        async def on_chat_message_received(self, mas_message: Message, chat_message: ChatMessage):
            if (mas_message.metadata[MasMessageMetadataFields.PERFORMATIVE.value] ==
                    MasMessagePerformatives.INFORM.value):
                # The doctor communicates that he is creating a new user
                await self.messaging_platform.send_message(
                    chat_message.sender_id,
                    localize(NEW_USER_MESSAGE_NOT_LOCALIZED, chat_message.sender_locale)
                )
            else:
                # Default handling behaviour
                await super().on_chat_message_received(mas_message, chat_message)

        def extract_user_id(self, other_agent_message: Message) -> str:
            return UserFactory.from_json(other_agent_message.body).id

        async def handle_user_data_response(self, cached_user: CachedUser, mas_message: Message,
                                            chat_message: ChatMessage):
            await forward_message_to_user_agent(self, cached_user, mas_message, chat_message, mas_message.sender)

    def create_default_fsm_state(self) -> AbstractCheckUserRegistrationState:
        return self.create_check_user_registration_state(self.messaging_platform_api_token)

    def create_fsm_behaviour_message_template(self) -> Optional[Template]:
        return Template(to=self.jid_str, sender=self.messaging_platform_sender)

    @abstractmethod
    def create_check_user_registration_state(self, messaging_platform_api_token: str) -> \
            AbstractCheckUserRegistrationState:
        """A template method to create the concrete CheckUserRegistrationState needed by the agent"""
        pass

    @abstractmethod
    def create_handle_user_registration_response_state(self, messaging_platform_api_token: str) -> \
            AbstractHandleUserRegistrationResponseState:
        """A template method to create the concrete HandleUserRegistrationResponseState needed by the agent"""
        pass


async def forward_message_to_user_agent(
        behaviour: Union[
            AbstractCovid19GatewayAgent.AbstractCheckUserRegistrationState,
            AbstractCovid19GatewayAgent.AbstractHandleUserRegistrationResponseState
        ],
        cached_user: CachedUser,
        to_forward_message: Message,
        chat_message: ChatMessage,
        doctor_agent_jid: str
):
    """Utility function to handle the user agent startup"""

    async def before_create_user_agent():
        """Callback used to do something before agent creation"""

        if not chat_message.is_quick_reply:  # Show "typing..." in chat, if a message will follow
            await behaviour.messaging_platform.send_chat_action(chat_message.sender_id, ChatAction.TYPING)

    def create_agent(agent_jid: str, agent_cached_user: CachedUser):
        """Callback used to create the user agent"""

        log(behaviour.agent, f"Creating the UserAgent with jid {agent_jid}", logger)

        return UserAgent(
            jid=agent_jid,
            password=f"{agent_jid}",
            my_user_id=agent_cached_user.user_id,
            doctor_jid=str(doctor_agent_jid),
            default_platform_and_token=(
                chat_message.chat_platform,
                behaviour.agent.messaging_platform_api_token
            ),
            gateway_agents_jids=ALL_PLATFORMS_GATEWAY_AGENTS_JIDS,
            db_connection_manager=behaviour.agent.db_connection_manager
        )

    user_agent_jid = compose_user_agent_jid(
        cached_user.user_id,
        str(behaviour.agent.jid.domain)
    )

    await UserAgentStartupHandler.handle_agent_startup(
        to_startup_agent_jid=lambda: user_agent_jid,
        presence_manager=behaviour.agent.presence,
        on_agent_already_online=lambda user_jid: log(behaviour.agent, f"UserAgent {user_jid} already online.", logger),
        on_before_create_agent=before_create_user_agent,
        cached_user=cached_user,
        create_agent=create_agent
    )

    msg = to_forward_message
    msg.metadata[MESSAGING_PLATFORM_API_TOKEN_METADATA_FIELD] = behaviour.agent.messaging_platform_api_token
    msg.to = user_agent_jid
    msg.sender = msg.metadata[MasMessageMetadataFields.SENDER.value] = str(behaviour.agent.jid)
    log(behaviour.agent, f"Forwarding the messaging platform message to UserAgent {user_agent_jid}.", logger)
    await behaviour.send(msg)


CHECK_REGISTRATION_CONTACT_PARTIAL_NAME = "covid19_doctor"
"""The initial part of the name of the agent to be contacted for the user registration check"""
