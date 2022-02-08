import asyncio
import logging
import uuid
from abc import abstractmethod, ABC
from asyncio import Future
from dataclasses import dataclass
from typing import Optional, Callable, Awaitable, Mapping

from spade.agent import Agent
from spade.message import Message
from spade.presence import PresenceManager
from spade.template import Template

from common.agent.agents.custom_metadata_fields import MasMessageMetadataFields, MasMessagePerformatives
from common.agent.agents.interaction_texts import (
    localize, HELLO_MESSAGE_TEXT_NOT_LOCALIZED, NOT_FOUND_DOCTOR_AGENT_USER_MESSAGE_NOT_LOCALIZED,
    SORRY_INTERNAL_ERROR_TEXT_NOT_LOCALIZED
)
from common.agent.agents.my_abstract_agent import AbstractBaseFSMAgent
from common.agent.behaviour.abstract_fsm_state_behaviours import AbstractWaitForChatMessageState
from common.agent.behaviour.behaviours import WaitForMessageFSMBehaviour
from common.agent.my_logging import log
from common.agent.presence_utils import find_contact_by_partial_jid, is_agent_available, find_contact_by_partial_name
from common.chat.language_enum import Language
from common.chat.message.types import ChatMessage
from common.chat.platform.mixins import AbstractMessagingPlatformMixin

logger = logging.getLogger(__name__)


class AbstractGatewayAgent(AbstractBaseFSMAgent, ABC):
    """A class implementing an abstract Gateway Agent between a messaging platform and the Spade Multi-Agent System"""

    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.user_cache_manager: UserCacheManager = UserCacheManager()


@dataclass
class CachedUser:
    """A class representing cached User data"""

    user_id: str
    """The cached user ID"""

    user_agent_future: Optional[Future] = None
    """The future which will be completed once user UserAgent completes the start-up"""


class UserCacheManager:
    """A class to manage user cache"""

    def __init__(self):
        self._user_cache = {}

    def add_user(self, user_id: str, originating_message: ChatMessage) -> CachedUser:
        """
        Adds the provided user data to the user_cache

        :returns: The newly added Cached user
        """
        cached_user = CachedUser(user_id=user_id)
        self._user_cache[self._compose_key(originating_message)] = cached_user
        return cached_user

    def get_user(self, received_message: ChatMessage) -> Optional[CachedUser]:
        """Retrieves the CachedUser if present with the sender_id of the message"""
        return self._user_cache.get(self._compose_key(received_message), None)

    @staticmethod
    def _compose_key(message: ChatMessage):
        """Utility method to compose the key of the cache"""
        return f"{message.chat_platform.value}_{message.sender_id}"


class AbstractGatewayCachedMessageHandlingState(AbstractWaitForChatMessageState, ABC):
    """A template FSM behaviour state to handle messages from messaging platforms"""

    STATE_NAME = "AbstractGatewayCachedMessageHandlingState"

    async def on_chat_message_received(self, mas_message: Message, chat_message: ChatMessage):
        user_cache_manager: UserCacheManager = self.agent.user_cache_manager
        cached_user: CachedUser = user_cache_manager.get_user(chat_message)

        _first_name: Optional[str] = chat_message.sender_first_name
        _last_name: Optional[str] = chat_message.sender_last_name

        if cached_user is not None:
            log(self.agent, f"I have cached information about sender ID `{chat_message.sender_id}` "
                            f"{_first_name if _first_name else ''} {_last_name if _last_name else ''}. "
                            f"ID: {cached_user.user_id}", logger)

            await self.handle_already_cached_user(mas_message, chat_message, cached_user)
        else:
            log(self.agent, f"I haven't cached information about sender ID `{chat_message.sender_id}` "
                            f"{_first_name if _first_name else ''} {_last_name if _last_name else ''}. ", logger)

            await self.handle_not_cached_user(mas_message, chat_message)

    @abstractmethod
    async def handle_already_cached_user(self, mas_message: Message, chat_message: ChatMessage,
                                         cached_user: CachedUser):
        """Template method called when there is an already cached user for that messaging platform"""
        pass

    @abstractmethod
    async def handle_not_cached_user(self, mas_message: Message, chat_message: ChatMessage):
        """Template method called when there's no cached user for new messaging platform message"""
        pass

    async def add_cached_user(self, user_id: str, user_chat_message: ChatMessage) -> CachedUser:
        """
        A shorthand function to add a messaging platform user, to cached users

        :return: the cached user
        """

        user_cache_manager: UserCacheManager = self.agent.user_cache_manager
        return user_cache_manager.add_user(user_id, user_chat_message)


class AbstractUserDataResponseHandlingState(
    AbstractMessagingPlatformMixin, AbstractWaitForChatMessageState, ABC
):
    """A template FSM behaviour state handling the response about user data request"""

    STATE_NAME = "AbstractUserDataResponseHandlingState"

    def __init__(self, messaging_platform_api_token: str):
        # with multiple inheritance all constructors must be called explicitly
        super().__init__(messaging_platform_api_token)
        AbstractWaitForChatMessageState.__init__(self)

    async def on_chat_message_received(self, mas_message: Message, chat_message: ChatMessage):
        if mas_message.metadata[MasMessageMetadataFields.PERFORMATIVE.value] == \
                MasMessagePerformatives.INFORM_RESULT.value:

            _first_name: Optional[str] = chat_message.sender_first_name
            _last_name: Optional[str] = chat_message.sender_last_name
            log(self.agent,
                f"Received data for user ID `{chat_message.sender_id}` "
                f"{_first_name if _first_name else ''} "
                f"{_last_name if _last_name else ''}: "
                f"{mas_message.body}", logger)

            user_id = self.extract_user_id(mas_message)

            user_cache_manager: UserCacheManager = self.agent.user_cache_manager
            cached_user = user_cache_manager.add_user(user_id, chat_message)

            await self.handle_user_data_response(cached_user, mas_message, chat_message)
            log(self.agent, "Response received.", logger)

        elif mas_message.metadata[MasMessageMetadataFields.PERFORMATIVE.value] == MasMessagePerformatives.FAILURE.value:

            log(self.agent, f"The agent {mas_message.sender} informed me that it could not retrieve user data. "
                            f"The failure message is: "
                            f"`{mas_message.metadata[MasMessageMetadataFields.FAIL_MESSAGE.value]}`", logger)
            await self.handle_response_failure(mas_message, chat_message)
            log(self.agent, "Data retrieval failure.", logger, logging.WARNING)

        else:
            log(self.agent, f"Unrecognized performative in message: {mas_message}", logger, logging.ERROR)
            await self.handle_response_unknown_performative(mas_message, chat_message)
            log(self.agent, "Unrecognized performative.", logger, logging.ERROR)

        self.should_set_next_state = False  # This behaviour should be like a OneShotBehaviour, dies once executed

    @abstractmethod
    def extract_user_id(self, other_agent_message: Message) -> str:
        """Template method called when, upon receiving other agent response, we need to extract the user id"""
        pass

    @abstractmethod
    async def handle_user_data_response(self, cached_user: CachedUser, mas_message: Message, chat_message: ChatMessage):
        """Template method called after retrieving, and caching the user data"""
        pass

    async def handle_response_failure(self, mas_message: Message, chat_message: ChatMessage):
        """
        Method called when the response from the other agent is negative, on user data retrieval

        Defaults sending an internal error message
        """
        await self._send_internal_error_message(chat_message, SORRY_INTERNAL_ERROR_TEXT_NOT_LOCALIZED)

    async def handle_response_unknown_performative(self, mas_message: Message, chat_message: ChatMessage):
        """
        Template method called when the response performative could not be recognized

        Defaults sending an internal error message
        """
        await self._send_internal_error_message(chat_message, SORRY_INTERNAL_ERROR_TEXT_NOT_LOCALIZED)

    async def _send_internal_error_message(self, chat_message: ChatMessage,
                                           error_message_not_localized: Mapping[Language, str]):
        """A method to send back the provided error response"""

        await self.messaging_platform.send_message(
            chat_message.sender_id,
            localize(error_message_not_localized, chat_message.sender_locale)
        )


class AbstractAskForUserDataAboutMessageState(
    AbstractMessagingPlatformMixin, AbstractGatewayCachedMessageHandlingState, ABC
):
    """A template FSM behaviour state handling the request for data, towards another agent"""

    STATE_NAME = "AbstractAskForUserDataAboutMessageState"

    def __init__(self, messaging_platform_api_token: str, to_ask_agent_partial_name: str):
        # with multiple inheritance all constructors must be called explicitly
        super().__init__(messaging_platform_api_token)
        AbstractGatewayCachedMessageHandlingState.__init__(self)

        self._to_ask_agent_partial_name = to_ask_agent_partial_name

    def _retrieve_other_agent_contact(self) -> Optional[str]:
        """Internal function to retrieve the other agent contact"""
        return find_contact_by_partial_name(self._to_ask_agent_partial_name, self.presence)

    async def handle_not_cached_user(self, mas_message: Message, chat_message: ChatMessage):

        other_agent_jid = self._retrieve_other_agent_contact()
        log(self.agent, f"Asking {other_agent_jid} for information...", logger)

        await self.on_before_asking_other_agent(chat_message)

        if not is_agent_available(other_agent_jid, self.presence):
            log(self.agent, f"Not found an available {other_agent_jid} agent in contacts! Maybe it wasn't started.",
                logger, logging.ERROR)
            await self.on_other_agent_not_available(chat_message)
        else:
            _first_name: Optional[str] = chat_message.sender_first_name
            _last_name: Optional[str] = chat_message.sender_last_name
            msg = Message(
                to=other_agent_jid,
                sender=self.agent.jid_str,
                body=f"User ID {chat_message.sender_id} "
                     f"{_first_name if _first_name else ''} {_last_name if _last_name else ''}",
                metadata=chat_message.strings_dictionary  # transmits the entire received message, as metadata
            )

            msg.metadata[MasMessageMetadataFields.PERFORMATIVE.value] = MasMessagePerformatives.REQUEST.value
            msg.metadata[MasMessageMetadataFields.SENDER.value] = self.agent.jid_str

            unique_request_code = str(uuid.uuid4())
            msg.metadata[MasMessageMetadataFields.REQUEST_UNIQUE_CODE.value] = unique_request_code

            response_template = Template()
            response_template.metadata[MasMessageMetadataFields.REQUEST_UNIQUE_CODE.value] = unique_request_code

            self.agent.add_behaviour(
                self.create_response_handling_behaviour(),
                template=response_template
            )
            await self.send(msg)

    async def on_before_asking_other_agent(self, chat_message: ChatMessage):
        """Method called before asking the other agent for the user information"""

        if not chat_message.is_quick_reply:  # Send "Hi..." message only if a message will follow
            _first_name: Optional[str] = chat_message.sender_first_name
            await self.messaging_platform.send_message(
                chat_message.sender_id,
                f"{localize(HELLO_MESSAGE_TEXT_NOT_LOCALIZED, chat_message.sender_locale)}"
                f" {_first_name if _first_name else ''}!"
            )

    async def on_other_agent_not_available(self, chat_message: ChatMessage):
        """Method called when the other agent is not present in contacts, or its present but not available"""

        await self.messaging_platform.send_message(
            chat_message.sender_id,
            localize(NOT_FOUND_DOCTOR_AGENT_USER_MESSAGE_NOT_LOCALIZED, chat_message.sender_locale)
        )

    @abstractmethod
    def create_response_handling_behaviour(self) -> WaitForMessageFSMBehaviour:
        """Template method to create the response handing behaviour"""
        pass


class UserAgentStartupHandler:
    """
    An abstract handler for User agent startup, with hooks to personalize its parts,
    avoiding multiple (same-)agent instantiation
    """

    @staticmethod
    async def handle_agent_startup(
            to_startup_agent_jid: Callable[[], str],
            presence_manager: PresenceManager,
            on_agent_already_online: Callable[[str], None],
            on_before_create_agent: Callable[[], Awaitable[None]],
            cached_user: CachedUser,
            create_agent: Callable[[str, CachedUser], Agent],
    ):
        """
        This is the main function, which should be called to handle a User agent startup,
        personalizing provided strategies
        """

        agent_jid: str = to_startup_agent_jid()

        user_agent_contact: Optional[str] = find_contact_by_partial_jid(agent_jid, presence_manager)
        if is_agent_available(user_agent_contact, presence_manager):
            on_agent_already_online(agent_jid)
        else:
            await on_before_create_agent()

            if cached_user.user_agent_future is not None:
                logger.info(f"The agent with jid {agent_jid} is already being created, wait for it to be started")

            else:
                agent = create_agent(agent_jid, cached_user)

                cached_user.user_agent_future = asyncio.wrap_future(
                    asyncio.run_coroutine_threadsafe(
                        agent.start(),
                        loop=asyncio.get_running_loop()
                    )
                )

            await cached_user.user_agent_future
