import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Mapping, List, Optional, Any, Union

from aiogram.types import ParseMode

from common.agent.agents.abstract_user_agent import AbstractMessagingPlatformReceiveMessageState
from common.agent.agents.interaction_texts import (
    localize, localize_list, NOT_A_VALID_RESPONSE_TEXT_NOT_LOCALIZED, SELECT_ONE_OF_THE_OPTIONS_TEXT_NOT_LOCALIZED,
    LETS_COMPLETE_YOUR_PROFILE_MESSAGE_TEXT_NOT_LOCALIZED, I_DONT_UNDERSTAND_TEXT_NOT_LOCALIZED
)
from common.agent.my_logging import log
from common.chat.language_enum import Language
from common.chat.message.types import ChatActualMessage, ChatMessage
from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform, ChatAction
from common.database.user.abstract_user import AbstractBasicUser

logger = logging.getLogger(__name__)


class AbstractMessagingPlatformReceiveIgnoringMessageState(AbstractMessagingPlatformReceiveMessageState, ABC):
    """Abstract state class to manage relevant messages, ignoring provided ones"""

    STATE_NAME = "AbstractMenuOptionsHandlingState"

    def __init__(self, ignored_messages_not_localized: List[Mapping[Language, str]] = None):
        super().__init__()

        self._ignored_messages_not_localized = (
            ignored_messages_not_localized if ignored_messages_not_localized is not None else []
        )

        self.current_language: Optional[Language] = None

    async def on_start(self):
        await super().on_start()
        # NOTE: this gets called every time the user clicks something

        if not self.current_language:
            self.current_language = self.user.language

    async def handle_message(self, chat_actual_message: ChatActualMessage):
        await super().handle_message(chat_actual_message)
        msg_text = chat_actual_message.message_text
        if self._is_message_to_ignore(chat_actual_message):
            log(self.agent, f"Ignoring received message for {self.STATE_NAME}: `{msg_text}`", logger)
            await self.handle_ignored_message(chat_actual_message)
        else:
            await self.handle_not_ignored_message(chat_actual_message)

        self.current_language = None

    def _is_message_to_ignore(self, chat_message: ChatMessage):
        """Utility function encapsulating the logic to define if a message should be ignored or not"""
        return (
                chat_message.message_text in
                localize_list(self._ignored_messages_not_localized, self.current_language)
        )

    async def handle_ignored_message(self, chat_actual_message: ChatActualMessage):
        """Template method to handle an ignored message, defaults doing nothing"""
        pass

    @abstractmethod
    async def handle_not_ignored_message(self, chat_actual_message: ChatActualMessage):
        """Template method to handle a not ignored message"""
        pass

    def should_show_typing_in_chat(self, received_message: ChatMessage):
        # redefined to show typing only if the message is also not ignored
        return super().should_show_typing_in_chat(received_message) and not self._is_message_to_ignore(received_message)


# If at some point this class will be used in Profiles ChatBot the migration of the language field should be done
# before, and all the "patch" code to retain backwards compatibility should be removed from database classes
class AbstractMenuOptionsHandlingState(AbstractMessagingPlatformReceiveIgnoringMessageState, ABC):
    """Abstract state class to manage user menu options, and their sending"""

    STATE_NAME = "AbstractMenuOptionsHandlingState"

    def __init__(self,
                 question_text_not_localized: Mapping[Language, str],
                 available_options_not_localized: List[Mapping[Language, str]],
                 ignored_messages_not_localized: List[Mapping[Language, str]] = None,
                 contains_photo: bool = False
                 ):
        super().__init__(ignored_messages_not_localized)

        self._question_text_not_localized = question_text_not_localized
        self._available_options_not_localized = available_options_not_localized
        self.contains_photo = contains_photo

    async def handle_not_ignored_message(self, chat_actual_message: ChatActualMessage):
        msg_text = chat_actual_message.message_text
        if self.is_legal_option(chat_actual_message):
            log(self.agent, f"Received legal value for {self.STATE_NAME}: `{msg_text}`"
                            f" with ID `{chat_actual_message.message_id}`.", logger)
            await self.on_legal_value(self.user, chat_actual_message)
        else:
            log(self.agent, f"Received illegal value for {self.STATE_NAME}: `{msg_text}`"
                            f" with ID `{chat_actual_message.message_id}`.", logger)
            await self.on_illegal_value(chat_actual_message)

    def is_legal_option(self, chat_actual_message: ChatActualMessage) -> bool:
        """
        Function to determine if a value is legal.

        Defaults checking if available options include the user sent value
        """
        if self.contains_photo & (chat_actual_message.message_text == "photo"):
            return "photo" in chat_actual_message.strings_dictionary
        else:
            return chat_actual_message.message_text in localize_list(self._available_options_not_localized,
                                                                     self.current_language)

    @abstractmethod
    async def on_legal_value(self, user: AbstractBasicUser, chat_actual_message: ChatActualMessage):
        """Template method called to do something, upon receiving legal value"""
        pass

    async def on_illegal_value(self, chat_actual_message: ChatActualMessage):
        """
        Method called to handle illegal value received from user

        Defaults asking the user for the same question, with current options
        """
        if chat_actual_message.message_timestamp < self.messaging_platform.last_sent_message.message_timestamp:
            log(self.agent, f"Ignoring `{chat_actual_message.message_text}` because was sent by the user before "
                            f"last Bot message.", logger)
        else:
            log(self.agent, f"Asking again.", logger)
            await self.messaging_platform.send_message(
                chat_actual_message.sender_id,
                f"{localize(NOT_A_VALID_RESPONSE_TEXT_NOT_LOCALIZED, self.current_language)}\n\n"
                f"{localize(SELECT_ONE_OF_THE_OPTIONS_TEXT_NOT_LOCALIZED, self.current_language)}",
                reply_to_message_id=chat_actual_message.message_id,
                custom_keyboard_obj=self.messaging_platform_handling_strategies.create_menu_keyboard_from(
                    localize_list(self._available_options_not_localized, self.current_language)
                )
            )

    def current_localize(self, to_localize: Mapping[Language, str]):
        """Shorthand method to call "localize" method with current language set"""

        return localize(to_localize, self.current_language)


async def ask_question(
        messaging_platform: AbstractMessagingPlatform,
        recipient_id: str,
        question_text_not_localized: Mapping[Language, str],
        current_language: Optional[Language],
        custom_keyboard_obj: Any = None,
        quick_reply_menu_obj: Any = None,
        disable_web_page_preview: bool = False,
        parse_mode: Union[str, None] = ParseMode.MARKDOWN
) -> ChatMessage:
    """A method to ask the user a question; returns sent message"""

    return await messaging_platform.send_message_after_sleep(
        recipient_id,
        localize(question_text_not_localized, current_language),
        custom_keyboard_obj=custom_keyboard_obj,
        quick_reply_menu_obj=quick_reply_menu_obj,
        disable_web_page_preview=disable_web_page_preview,
        parse_mode=parse_mode
    )


class AbstractUserRegistrationCheckingState(AbstractMessagingPlatformReceiveIgnoringMessageState, ABC):
    """Abstract state class to manage user registration, is not completed"""

    STATE_NAME = "AbstractUserRegistrationCheckingState"

    def __init__(self, ignored_messages_not_localized: List[Mapping[Language, str]] = None):
        super().__init__(ignored_messages_not_localized)

    async def handle_not_ignored_message(self, chat_actual_message: ChatActualMessage):
        msg_text = chat_actual_message.message_text
        current_chat_platform = chat_actual_message.chat_platform.value
        log(self.agent, f"Will handle `{msg_text}` from `{current_chat_platform}` "
                        f"with ID `{chat_actual_message.message_id}`", logger)
        user, language = self.user, self.user.language
        sender_id: str = chat_actual_message.sender_id

        if not await self.check_user_completed_registration(user):
            await self.messaging_platform.send_message(
                sender_id,
                localize(self.bot_introduction_message_text_not_localized(), language),
                custom_keyboard_obj=(
                    self.messaging_platform_handling_strategies.create_show_normal_keyboard()
                )
            )
            await self.messaging_platform.send_chat_action(sender_id, ChatAction.TYPING)
            await asyncio.sleep(2)
            await self.messaging_platform.send_message(
                sender_id,
                localize(LETS_COMPLETE_YOUR_PROFILE_MESSAGE_TEXT_NOT_LOCALIZED, language)
            )
            await self.messaging_platform.send_chat_action(sender_id, ChatAction.TYPING)
            await asyncio.sleep(1)
            await self.start_registration_process(chat_actual_message)
        else:
            if await self.dispatch_commands(chat_actual_message):
                log(self.agent, f"Completed handling of `{msg_text}` with ID `{chat_actual_message.message_id}` "
                                f"from `{current_chat_platform}`", logger)
            else:
                log(self.agent,
                    f"Not implemented command in behaviour for {current_chat_platform} `{msg_text}` "
                    f"with ID `{chat_actual_message.message_id}`",
                    logger, logging.ERROR)

                await self.messaging_platform.send_message(
                    sender_id,
                    localize(I_DONT_UNDERSTAND_TEXT_NOT_LOCALIZED, language),
                    reply_to_message_id=chat_actual_message.message_id
                )
                await self.send_help_string(chat_actual_message)

    @abstractmethod
    async def check_user_completed_registration(self, user: AbstractBasicUser) -> bool:
        """Template method to determine if the user already completed the registration process"""
        pass

    @abstractmethod
    def bot_introduction_message_text_not_localized(self) -> Mapping[Language, str]:
        """Template property to gather the introduction message of the bot"""
        pass

    @abstractmethod
    async def start_registration_process(self, chat_actual_message: ChatActualMessage):
        """Template method to start the registration process, if the user wasn't registered"""
        pass

    @abstractmethod
    async def dispatch_commands(self, chat_actual_message: ChatActualMessage) -> bool:
        """
        Template method to dispatch specific commands

        This method should return True if the command was understood, False otherwise (triggering error message sending)
        """
        pass

    @abstractmethod
    async def send_help_string(self, chat_actual_message: ChatActualMessage):
        """Template method to send the help string, when the user sends an unknown command"""
        pass
