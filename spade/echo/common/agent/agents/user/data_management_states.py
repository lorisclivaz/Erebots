import asyncio
import logging
from abc import ABC
from threading import Timer
from typing import List, Optional, Callable, Awaitable, Mapping

from common.agent.agents.interaction_texts import localize_list
from common.agent.behaviour.abstract_user_agent_behaviours import AbstractMenuOptionsHandlingState, ask_question
from common.agent.my_logging import log
from common.chat.language_enum import Language
from common.chat.message.types import ChatQuickReply, ChatMessage, ChatActualMessage
from common.pryv.api_wrapper import PryvAPI
from common.pryv.model import DataAccessPermission, AuthStatus, AuthResponse
from common.utils.dictionaries import inverse_dictionary
from echo.common.agent.agents.interaction_texts import (
    IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED, LANGUAGE_QUESTION_TEXT_NOT_LOCALIZED,
    ECHO_TEXT_NOT_LOCALIZED, PRYV_ACCESS_ASKING_TEXT_NOT_LOCALIZED,
    YES_BUTTON_TEXT_NOT_LOCALIZED, NO_BUTTON_TEXT_NOT_LOCALIZED,
    REGISTRATION_IS_MANDATORY_TO_USE_BOT_TEXT_NOT_LOCALIZED,
    PERFECT_YOU_CAN_DO_IT_WITH_FOLLOWING_LINK_TEXT_NOT_LOCALIZED,
    WAITING_FOR_PRYV_REGISTRATION_MESSSAGE_TEXT_NOT_LOCALIZED, PRYV_ACCESS_CONFIRMED_MESSAGE_TEXT_NOT_LOCALIZED
)
from echo.common.agent.agents.user.abstract_behaviours import AbstractEchoReceiveMessageState
from echo.common.database.mongo_db_pryv_hybrid.models import PryvStoredData
from echo.common.database.user.model.abstract_user import AbstractUser
from common.pryv.server_domain import PRYV_PROJECT_ID

logger = logging.getLogger(__name__)


async def ask_for_next_missing_field_or_complete_registration(
        state: AbstractEchoReceiveMessageState,
        recipient_id: str,
        on_registration_completed_callback: Callable[[AbstractEchoReceiveMessageState, str], Awaitable[None]],
):
    """Utility function to ask next missing info, or complete the registration process (if applicable)"""

    user: AbstractUser = state.user
    language = user.language

    if user.pryv_endpoint is None:
        await PryvAccessAskingState.ask_for_pryv_access(state, recipient_id, language)
    elif user.language is None:
        await LanguageInsertionState.ask_for_language(state, recipient_id, language)
    else:
        log(state.agent, f"User registration completed!", logger)
        user.registration_completed = True
        await on_registration_completed_callback(state, recipient_id)


class AbstractDataInsertionState(AbstractMenuOptionsHandlingState, AbstractEchoReceiveMessageState, ABC):
    """An abstract state specific for the data handling phase (insertion/modification)"""

    STATE_NAME = "AbstractDataInsertionState"

    def __init__(self, question_text_not_localized: Mapping[Language, str],
                 available_options_not_localized: List[Mapping[Language, str]],
                 default_quick_reply_handler: Callable[
                     [AbstractEchoReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractEchoReceiveMessageState, str], Awaitable[None]],
                 ignored_messages_not_localized: List[Mapping[Language, str]],
                 ):
        AbstractMenuOptionsHandlingState.__init__(
            self, question_text_not_localized, available_options_not_localized, ignored_messages_not_localized
        )
        AbstractEchoReceiveMessageState.__init__(self)

        self._default_quick_reply_handler = default_quick_reply_handler
        self._on_registration_completed_callback = on_registration_completed

    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        await self._default_quick_reply_handler(self, chat_quick_reply)

    async def proceed_to_next_state(self, user: AbstractUser, recipient_id: str):
        """Utility method to encapsulate the logic of proceeding to next state"""

        if not user.registration_completed:
            await ask_for_next_missing_field_or_complete_registration(
                self, recipient_id, self._on_registration_completed_callback
            )


class PryvAccessAskingState(AbstractDataInsertionState):
    """A FSM State to handle user Pryv access asking"""

    STATE_NAME = "PryvAccessAskingState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [
        YES_BUTTON_TEXT_NOT_LOCALIZED,
        NO_BUTTON_TEXT_NOT_LOCALIZED
    ]

    ALTERNATIVE_KEYBOARD_OPTIONS_NOT_LOCALIZED = [
        IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED
    ]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractEchoReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractEchoReceiveMessageState, str], Awaitable[None]],
                 get_pryv_api: Callable[[], PryvAPI],
                 ):
        super().__init__(PRYV_ACCESS_ASKING_TEXT_NOT_LOCALIZED, PryvAccessAskingState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, [])

        self.get_pryv_api = get_pryv_api

        self.pryv_api: Optional[PryvAPI] = None
        self.message_with_link: Optional[ChatMessage] = None

    async def on_start(self):
        await super().on_start()

        if self.pryv_api is None:
            self.pryv_api = self.get_pryv_api()

    def _is_message_to_ignore(self, chat_message: ChatMessage):
        return super()._is_message_to_ignore(chat_message) or (
                self.messaging_platform.last_sent_message.message_timestamp > chat_message.message_timestamp
        )

    def is_legal_option(self, chat_actual_message: ChatActualMessage) -> bool:
        received_value: str = chat_actual_message.message_text
        return (
                received_value in localize_list(self.KEYBOARD_OPTIONS_NOT_LOCALIZED, self.current_language) or
                received_value in localize_list(self.ALTERNATIVE_KEYBOARD_OPTIONS_NOT_LOCALIZED,
                                                self.current_language)
        )

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        if IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED not in self._available_options_not_localized:
            if legal_value == self.current_localize(YES_BUTTON_TEXT_NOT_LOCALIZED):
                log(self.agent, f"Start pryv registration process...")

                auth_response = self.pryv_api.request_auth(
                    requesting_app_id=PRYV_PROJECT_ID,
                    requested_permissions=[
                        DataAccessPermission.of(info[0], info[1], info[2])
                        for info in PryvStoredData.values()
                    ]
                )

                self.message_with_link = await self.messaging_platform.send_message_after_sleep(
                    sender_id,
                    f"{self.current_localize(PERFECT_YOU_CAN_DO_IT_WITH_FOLLOWING_LINK_TEXT_NOT_LOCALIZED)}\n"
                    f"{auth_response.auth_url}",
                    custom_keyboard_obj=self.messaging_platform_handling_strategies.create_menu_keyboard_from(
                        localize_list(self.ALTERNATIVE_KEYBOARD_OPTIONS_NOT_LOCALIZED, self.current_language)
                    )
                )
                self._available_options_not_localized = self.ALTERNATIVE_KEYBOARD_OPTIONS_NOT_LOCALIZED

                await self.poll_for_access_granting(sender_id, self.current_language, auth_response)

            elif legal_value == self.current_localize(NO_BUTTON_TEXT_NOT_LOCALIZED):
                await self.persuade_user_to_grant_access(sender_id)
            elif legal_value == self.current_localize(IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED):
                pass
                # Ignore this case because this button was pressed before the keyboard reset,
                # and a response has already been sent
            else:
                log(self.agent,
                    f"Not implemented case!! `{legal_value}` was added to legal values but it's not handled!",
                    logger, logging.ERROR)
        elif legal_value == self.current_localize(IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED) and self.user.pryv_endpoint:
            await self.messaging_platform.send_message_after_sleep(
                sender_id,
                self.current_localize(PRYV_ACCESS_CONFIRMED_MESSAGE_TEXT_NOT_LOCALIZED)
            )
            # Delete old link message to clean user chat
            await self.delete_link_message(sender_id)
            self._reset_state_to_initial_condition()

            # Bulk creates the initial stream structure
            self.pryv_api.create_stream_structure(self.user.pryv_endpoint)

            await self.proceed_to_next_state(self.user, sender_id)
        else:
            log(self.agent, f"User already expressed his's initial positive consent, now waiting for "
                            f"his consent on Pryv", logger)
            await self.messaging_platform.send_message_after_sleep(
                sender_id,
                self.current_localize(WAITING_FOR_PRYV_REGISTRATION_MESSSAGE_TEXT_NOT_LOCALIZED),
                sleep_seconds=2
            )

    def _reset_state_to_initial_condition(self):
        """Utility function to reset the state to the initial condition"""
        self._available_options_not_localized = self.KEYBOARD_OPTIONS_NOT_LOCALIZED

    async def delete_link_message(self, recipient_id: str):
        """Link message deletion handler"""
        await self.messaging_platform.delete_message(
            recipient_id,
            self.message_with_link.message_id
        )
        self.message_with_link = None

    async def persuade_user_to_grant_access(self, sender_id: str):
        """Utility function to ask the user to grant access because it's mandatory to continue"""
        await self.messaging_platform.send_message_after_sleep(
            sender_id,
            self.current_localize(REGISTRATION_IS_MANDATORY_TO_USE_BOT_TEXT_NOT_LOCALIZED)
        )
        await self.proceed_to_next_state(self.user, sender_id)

    async def poll_for_access_granting(
            self, recipient_id: str, current_language: Optional[Language], auth_response: AuthResponse
    ):
        """Function to poll the Pryv api to verify if the user granted access authorization"""

        next_auth_response = self.pryv_api.fetch_poll_url(auth_response)
        if next_auth_response.status == AuthStatus.ACCEPTED:
            log(self.agent, f"User gave Pryv access to our Bot.", logger)
            self.user.pryv_endpoint = next_auth_response.pryv_api_endpoint

        elif next_auth_response.status == AuthStatus.REFUSED:
            log(self.agent, f"User refused to give Pryv access.", logger)
            self._reset_state_to_initial_condition()
            await self.persuade_user_to_grant_access(recipient_id)

            # Delete old link message to clean user chat
            await self.delete_link_message(recipient_id)
        elif next_auth_response.status == AuthStatus.NEED_SIGNIN:
            log(self.agent, f"Not accepted yet", logger)
            Timer(
                next_auth_response.poll_rate_ms / 1000,
                asyncio.gather,
                [self.poll_for_access_granting(recipient_id, current_language, next_auth_response)],
                {'loop': asyncio.get_running_loop()}
            ).start()
        else:
            log(self.agent, f"Unknown auth response status: {next_auth_response.status}", logger, logging.ERROR)

    @staticmethod
    async def ask_for_pryv_access(current_state: AbstractEchoReceiveMessageState, recipient_id: str,
                                  current_language: Optional[Language]) -> ChatMessage:
        """Utility method to ask for Pryv access"""

        current_state.set_next_state(PryvAccessAskingState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            PRYV_ACCESS_ASKING_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(PryvAccessAskingState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            )
        )


class LanguageInsertionState(AbstractDataInsertionState):
    """A FSM State to handle user Language insertion"""

    STATE_NAME = "LanguageInsertionState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [
        {Language.LANGUAGE_ENGLISH: language}
        for language in Language.pretty_values()
    ]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractEchoReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ], on_registration_completed: Callable[[AbstractEchoReceiveMessageState, str], Awaitable[None]],
                 ):
        super().__init__(LANGUAGE_QUESTION_TEXT_NOT_LOCALIZED, LanguageInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, [])

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        uglyfier_dictionary = inverse_dictionary(Language.values_prettifier_dictionary())
        user.language = Language(uglyfier_dictionary[legal_value])

        await self.proceed_to_next_state(user, sender_id)

    @staticmethod
    async def ask_for_language(current_state: AbstractEchoReceiveMessageState, recipient_id: str,
                               current_language: Optional[Language]) -> ChatMessage:
        """Utility method to ask for Language"""

        current_state.set_next_state(LanguageInsertionState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            LANGUAGE_QUESTION_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(LanguageInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            )
        )


class EchoState(AbstractMenuOptionsHandlingState, AbstractEchoReceiveMessageState):
    """A FSM State to handle user Name insertion"""

    STATE_NAME = "EchoState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractEchoReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractEchoReceiveMessageState, str, bool], Awaitable[None]],
                 ):

        AbstractMenuOptionsHandlingState.__init__(
            self, ECHO_TEXT_NOT_LOCALIZED,
            EchoState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
            ignored_messages_not_localized=[
                *LanguageInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED
            ]
        )
        AbstractEchoReceiveMessageState.__init__(self)

        self._default_quick_reply_handler = default_quick_reply_handler
        self._on_back_to_menu_with_optional_message = on_back_to_menu

    def is_legal_option(self, chat_actual_message: ChatActualMessage) -> bool:
        return True  # Everything goes.

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        if legal_value == self.current_localize(IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED):
            await self._on_back_to_menu_with_optional_message(self, sender_id, True)
        else:
            await self.messaging_platform.send_message_after_sleep(
                recipient_id=sender_id,
                message_text=legal_value
            )

    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        await self._default_quick_reply_handler(self, chat_quick_reply)

    @staticmethod
    async def start_echo(current_state: AbstractEchoReceiveMessageState, recipient_id: str,
                         current_language: Optional[Language]) -> ChatMessage:
        """Utility method to start the Echo state"""

        current_state.set_next_state(EchoState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            ECHO_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(EchoState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            )
        )
