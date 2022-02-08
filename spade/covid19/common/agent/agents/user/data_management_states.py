import asyncio
import logging
from abc import ABC
from threading import Timer
from typing import List, Collection, Optional, Set, Any, Callable, Awaitable, Mapping

from common.agent.agents.interaction_texts import markup_text, localize, localize_list
from common.agent.behaviour.abstract_user_agent_behaviours import AbstractMenuOptionsHandlingState, ask_question
from common.agent.my_logging import log
from common.chat.language_enum import Language
from common.chat.message.types import ChatQuickReply, ChatMessage, ChatActualMessage
from common.pryv.api_wrapper import PryvAPI
from common.pryv.model import DataAccessPermission, AuthResponse, AuthStatus
from common.utils.dictionaries import inverse_dictionary
from covid19.common.agent.agents.interaction_texts import (
    AGE_QUESTION_TEXT_NOT_LOCALIZED, SEX_QUESTION_TEXT_NOT_LOCALIZED, FAVOURITE_SPORT_DAYS_QUESTION_TEXT_NOT_LOCALIZED,
    SUPPLEMENTARY_FAVOURITE_SPORT_DAYS_QUESTION_TEXT_NOT_LOCALIZED, GOALS_QUESTION_TEXT_NOT_LOCALIZED,
    IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED, WHICH_DATA_TO_UPDATE_QUESTION_TEXT_NOT_LOCALIZED,
    NAME_TEXT_NOT_LOCALIZED, LANGUAGE_TEXT_NOT_LOCALIZED, SEX_TEXT_NOT_LOCALIZED,
    AGE_TEXT_NOT_LOCALIZED, FAVOURITE_SPORT_DAYS_TEXT_NOT_LOCALIZED, GOALS_TEXT_NOT_LOCALIZED,
    SELECT_OPTION_TEXT_NOT_LOCALIZED, DESELECT_OPTION_TEXT_NOT_LOCALIZED, select_at_least_goals_text_not_localized,
    BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED, still_missing_text_not_localized, DAY_TEXT_NOT_LOCALIZED,
    MODIFY_FAVOURITE_SPORT_DAYS_OPTION_TEXT_NOT_LOCALIZED, LANGUAGE_QUESTION_TEXT_NOT_LOCALIZED,
    NAME_QUESTION_TEXT_NOT_LOCALIZED, DAYS_TEXT_NOT_LOCALIZED, LETS_EVALUATE_YOUR_ABILITY_MESSAGE_TEXT,
    REDO_EVALUATION_TEXT_NOT_LOCALIZED, LEVEL_TEXT_NOT_LOCALIZED, PRYV_ACCESS_ASKING_TEXT_NOT_LOCALIZED,
    YES_BUTTON_TEXT_NOT_LOCALIZED, NO_BUTTON_TEXT_NOT_LOCALIZED,
    REGISTRATION_IS_MANDATORY_TO_USE_BOT_TEXT_NOT_LOCALIZED,
    PERFECT_YOU_CAN_DO_IT_WITH_FOLLOWING_LINK_TEXT_NOT_LOCALIZED,
    WAITING_FOR_PRYV_REGISTRATION_MESSSAGE_TEXT_NOT_LOCALIZED, PRYV_ACCESS_CONFIRMED_MESSAGE_TEXT_NOT_LOCALIZED
)
from covid19.common.agent.agents.level_model import compute_user_level
from covid19.common.agent.agents.user.abstract_behaviours import (
    AbstractCovid19ReceiveMessageState
)
from covid19.common.agent.available_functionality_enums import UserFunctionality
from covid19.common.database.enums import AgeField, SexField, WeekDayField
from covid19.common.database.mongo_db_pryv_hybrid.models import PryvStoredData
from covid19.common.database.user.field_enums import ShiftField, DifficultyField
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal

logger = logging.getLogger(__name__)

NEEDED_FAVOURITE_DAYS_COUNT = 3
"""The number of required user favourite week days for doing sport"""

NEEDED_SELF_GOALS_COUNT = 1
"""The number of required user goals, to be set"""


async def ask_for_next_missing_field_or_complete_registration(
        state: AbstractCovid19ReceiveMessageState,
        recipient_id: str,
        on_registration_completed_callback: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
        get_user_available_goals: Callable[[], List[AbstractUserGoal]],
        get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
):
    """Utility function to ask next missing info, or complete the registration process (if applicable)"""

    user: AbstractUser = state.user
    language = user.language

    if user.pryv_endpoint is None:
        await PryvAccessAskingState.ask_for_pryv_access(state, recipient_id, language)
    elif user.language is None:
        await LanguageInsertionState.ask_for_language(state, recipient_id, language)
    elif user.first_name is None:
        await NameInsertionState.ask_for_name(state, recipient_id, language)
    elif user.sex is None:
        await SexInsertionState.ask_for_sex(state, recipient_id, language)
    elif user.age is None:
        await AgeInsertionState.ask_for_age(state, recipient_id, language)
    elif not user.favourite_sport_days:
        await FavouriteWeekDaysInsertionState.ask_for_favourite_sport_days(state, recipient_id, language)
    elif not user.goals:
        await GoalSettingState.ask_for_goals(
            state, recipient_id, language, get_user_available_goals()
        )
    elif not user.current_question or not user.current_question_answer:
        await UserEvaluationQuestionsState.start_user_evaluation_process(
            state, recipient_id, language, get_evaluation_questions
        )
    else:
        log(state.agent, f"User registration completed!", logger)
        user.registration_completed = True
        await on_registration_completed_callback(state, recipient_id)


class AbstractDataInsertionState(AbstractMenuOptionsHandlingState, AbstractCovid19ReceiveMessageState, ABC):
    """An abstract state specific for the data handling phase (insertion/modification)"""

    STATE_NAME = "AbstractDataInsertionState"

    def __init__(self, question_text_not_localized: Mapping[Language, str],
                 available_options_not_localized: List[Mapping[Language, str]],
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ignored_messages_not_localized: List[Mapping[Language, str]],
                 ):

        AbstractMenuOptionsHandlingState.__init__(
            self, question_text_not_localized, available_options_not_localized, ignored_messages_not_localized
        )
        AbstractCovid19ReceiveMessageState.__init__(self)

        self._default_quick_reply_handler = default_quick_reply_handler
        self._on_registration_completed_callback = on_registration_completed
        self._get_user_available_goals = get_user_available_goals
        self._get_evaluation_questions = get_evaluation_questions

    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        await self._default_quick_reply_handler(self, chat_quick_reply)

    async def proceed_to_next_state(self, user: AbstractUser, recipient_id: str):
        """Utility method to encapsulate the logic of proceeding to next state"""

        if not user.registration_completed:
            await ask_for_next_missing_field_or_complete_registration(
                self, recipient_id, self._on_registration_completed_callback, self._get_user_available_goals,
                self._get_evaluation_questions
            )
        else:
            await UpdatePersonalDataState.ask_for_what_to_update(self, recipient_id, user)


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
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 get_pryv_api: Callable[[], PryvAPI],
                 ):
        super().__init__(PRYV_ACCESS_ASKING_TEXT_NOT_LOCALIZED, PryvAccessAskingState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, get_user_available_goals,
                         get_evaluation_questions,
                         [
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED
                         ])

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

    def is_legal_option(self, received_value: str) -> bool:
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
                    requesting_app_id='covid19-physio-project',
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
    async def ask_for_pryv_access(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
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
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ], on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):
        super().__init__(LANGUAGE_QUESTION_TEXT_NOT_LOCALIZED, LanguageInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, get_user_available_goals,
                         get_evaluation_questions,
                         [
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         ])

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        uglyfier_dictionary = inverse_dictionary(Language.values_prettifier_dictionary())
        user.language = Language(uglyfier_dictionary[legal_value])

        await self.proceed_to_next_state(user, sender_id)

    @staticmethod
    async def ask_for_language(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
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


class NameInsertionState(AbstractDataInsertionState):
    """A FSM State to handle user Name insertion"""

    STATE_NAME = "NameInsertionState"

    KEYBOARD_OPTIONS = []

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ], on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):
        super().__init__(NAME_QUESTION_TEXT_NOT_LOCALIZED, NameInsertionState.KEYBOARD_OPTIONS,
                         default_quick_reply_handler, on_registration_completed, get_user_available_goals,
                         get_evaluation_questions,
                         [
                             *LanguageInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED
                         ])

    def is_legal_option(self, received_value: str) -> bool:
        return True  # Legality check for name

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        sender_id: str = chat_actual_message.sender_id
        user.first_name = chat_actual_message.message_text

        await self.proceed_to_next_state(user, sender_id)

    @staticmethod
    async def ask_for_name(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                           current_language: Optional[Language]) -> ChatMessage:
        """Utility method to ask for Name"""

        current_state.set_next_state(NameInsertionState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            NAME_QUESTION_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                NameInsertionState.KEYBOARD_OPTIONS
            )
        )


class SexInsertionState(AbstractDataInsertionState):
    """A FSM State to handle user Sex insertion"""

    STATE_NAME = "SexInsertionState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = SexField.pretty_values_not_localized()

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ], on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):
        super().__init__(SEX_QUESTION_TEXT_NOT_LOCALIZED, SexInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, get_user_available_goals,
                         get_evaluation_questions, [
                             *NameInsertionState.KEYBOARD_OPTIONS,
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         ])

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        sender_id: str = chat_actual_message.sender_id
        user.sex = SexField(SexField.uglify(chat_actual_message.message_text))

        await self.proceed_to_next_state(user, sender_id)

    @staticmethod
    async def ask_for_sex(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                          current_language: Optional[Language]) -> ChatMessage:
        """Utility method to ask for Sex data"""

        current_state.set_next_state(SexInsertionState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            SEX_QUESTION_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(SexInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            )
        )


class AgeInsertionState(AbstractDataInsertionState):
    """A FSM State to handle user Age insertion"""

    STATE_NAME = "AgeInsertionState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = AgeField.pretty_values_not_localized()

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):
        super().__init__(AGE_QUESTION_TEXT_NOT_LOCALIZED, AgeInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, get_user_available_goals,
                         get_evaluation_questions, [
                             *SexInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         ])

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        sender_id: str = chat_actual_message.sender_id
        user.age = AgeField(AgeField.uglify(chat_actual_message.message_text))

        await self.proceed_to_next_state(user, sender_id)

    @staticmethod
    async def ask_for_age(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                          current_language: Optional[Language]) -> ChatMessage:
        """Utility method to ask for Age data"""

        current_state.set_next_state(AgeInsertionState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            AGE_QUESTION_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(AgeInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            )
        )


class FavouriteWeekDaysInsertionState(AbstractDataInsertionState):
    """A FSM State to handle user Favourite days insertion"""

    STATE_NAME = "FavouriteWeekDaysInsertionState"

    NEEDED_DAYS = NEEDED_FAVOURITE_DAYS_COUNT
    """The total number of days required to continue"""

    KEYBOARD_OPTIONS_NOT_LOCALIZED = WeekDayField.pretty_values_not_localized()

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):
        super().__init__(FAVOURITE_SPORT_DAYS_QUESTION_TEXT_NOT_LOCALIZED,
                         FavouriteWeekDaysInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, get_user_available_goals,
                         get_evaluation_questions, [
                             *AgeInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         ])

        self.selected_days: List[WeekDayField] = []

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        if legal_value != self.current_localize(IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED):
            self.selected_days.append(WeekDayField(WeekDayField.uglify(legal_value)))

        if (legal_value == self.current_localize(IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED)
                or len(self.selected_days) == len(self.KEYBOARD_OPTIONS_NOT_LOCALIZED)):
            user.favourite_sport_days = self.selected_days
            self.selected_days.clear()
            self._available_options_not_localized = self.KEYBOARD_OPTIONS_NOT_LOCALIZED

            await self.proceed_to_next_state(user, sender_id)

        elif len(self.selected_days) < self.NEEDED_DAYS:
            self._available_options_not_localized = [
                pretty_not_localized
                for day_value, pretty_not_localized in WeekDayField.values_prettifier_not_localized().items()
                if WeekDayField(day_value) not in self.selected_days
            ]
            await FavouriteWeekDaysInsertionState.ask_for_favourite_sport_days(
                self, sender_id, current_language=user.language,
                options_not_localized=self._available_options_not_localized,
                missing_count=self.NEEDED_DAYS - len(self.selected_days)
            )
        else:
            self._available_options_not_localized = [
                pretty_not_localized
                for day_value, pretty_not_localized in WeekDayField.values_prettifier_not_localized().items()
                if WeekDayField(day_value) not in self.selected_days
            ]
            self._available_options_not_localized.append(IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED)
            await FavouriteWeekDaysInsertionState.ask_for_supplementary_sport_days(
                self, sender_id, user.language, self._available_options_not_localized
            )

    @staticmethod
    async def ask_for_favourite_sport_days(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                           current_language: Optional[Language],
                                           options_not_localized: Collection[Mapping[Language, str]] = tuple(
                                               WeekDayField.pretty_values_not_localized()
                                           ),
                                           missing_count: int = NEEDED_DAYS) -> ChatMessage:
        """Utility method to ask for Favourite sport days data, defaulting in asking for all needed days"""

        missing_days_string_not_localized = still_missing_text_not_localized(
            DAY_TEXT_NOT_LOCALIZED, DAYS_TEXT_NOT_LOCALIZED, missing_count
        )

        question_not_localized = {
            language: (
                f"{fav_days_question_text} "
                f"{markup_text(localize(missing_days_string_not_localized, language), bold=True)}"
            )
            for language, fav_days_question_text in FAVOURITE_SPORT_DAYS_QUESTION_TEXT_NOT_LOCALIZED.items()
        }

        current_state.set_next_state(FavouriteWeekDaysInsertionState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            question_not_localized,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(options_not_localized, current_language)
            )
        )

    @staticmethod
    async def ask_for_supplementary_sport_days(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                               current_language: Optional[Language],
                                               options_not_localized: Collection[
                                                   Mapping[Language, str]
                                               ]) -> ChatMessage:
        """Utility method to ask for supplementary preference, about week days"""

        current_state.set_next_state(FavouriteWeekDaysInsertionState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            SUPPLEMENTARY_FAVOURITE_SPORT_DAYS_QUESTION_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(options_not_localized, current_language)
            )
        )


class GoalSettingState(AbstractDataInsertionState):
    """A FSM state to handle user goals setting"""

    STATE_NAME = "GoalSettingState"

    NEEDED_GOALS = NEEDED_SELF_GOALS_COUNT

    LEFT_OPTION_NOT_LOCALIZED = ShiftField.values_prettifier_not_localized()[ShiftField.PREVIOUS.value]
    RIGHT_OPTION_NOT_LOCALIZED = ShiftField.values_prettifier_not_localized()[ShiftField.NEXT.value]
    SELECT_OPTION_NOT_LOCALIZED = SELECT_OPTION_TEXT_NOT_LOCALIZED
    DESELECT_OPTION_NOT_LOCALIZED = DESELECT_OPTION_TEXT_NOT_LOCALIZED

    QUICK_OPTIONS_MENU_NOT_LOCALIZED = [
        LEFT_OPTION_NOT_LOCALIZED,
        SELECT_OPTION_NOT_LOCALIZED,
        RIGHT_OPTION_NOT_LOCALIZED
    ]
    QUICK_OPTIONS_MENU_SELECTED_NOT_LOCALIZED = [
        LEFT_OPTION_NOT_LOCALIZED,
        DESELECT_OPTION_NOT_LOCALIZED,
        RIGHT_OPTION_NOT_LOCALIZED
    ]

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):
        super().__init__(GOALS_QUESTION_TEXT_NOT_LOCALIZED, GoalSettingState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_registration_completed, get_user_available_goals,
                         get_evaluation_questions, [
                             *FavouriteWeekDaysInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         ])

        self._available_goals: Optional[List[AbstractUserGoal]] = None

        self.selected_goal_ids: Optional[Set[str]] = None
        self.currently_selected_index: int = 0

    async def on_start(self):
        await super().on_start()
        # NOTE: this gets called every time the user clicks something

        self._available_goals: List[AbstractUserGoal] = self._get_user_available_goals()

        if self.selected_goal_ids is None:
            user_goals = self.user.goals
            self.selected_goal_ids = set([goal.id for goal in user_goals]) if user_goals else set()

    def is_legal_option(self, chat_actual_message: ChatActualMessage) -> bool:
        return super().is_legal_option(chat_actual_message) and len(self.selected_goal_ids) >= self.NEEDED_GOALS

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        sender_id: str = chat_actual_message.sender_id
        await self.messaging_platform.edit_message(
            sender_id,
            self.messaging_platform.last_sent_message.message_id,
            self.current_localize(
                self.render_goals_not_localized(
                    GoalSettingState._selected_goals(self.selected_goal_ids, self._available_goals)
                )
            )
        )

        user.goals = [goal for goal in self._available_goals if goal.id in self.selected_goal_ids]

        # Cleanup data structures
        self.selected_goal_ids: Optional[Set[str]] = None
        self.currently_selected_index = 0

        await self.proceed_to_next_state(user, sender_id)

    async def on_illegal_value(self, chat_actual_message: ChatActualMessage):
        await self.messaging_platform.delete_message(
            chat_actual_message.sender_id,
            self.messaging_platform.last_sent_message.message_id
        )

        await self.messaging_platform.send_message_after_sleep(
            chat_actual_message.sender_id,
            self.current_localize(select_at_least_goals_text_not_localized(self.NEEDED_GOALS)),
            reply_to_message_id=chat_actual_message.message_id
        )
        await GoalSettingState.ask_for_goals(self, chat_actual_message.sender_id, self.current_language,
                                             self._available_goals, self.selected_goal_ids,
                                             self.currently_selected_index)

    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        payload = chat_quick_reply.quick_reply_payload
        localized_options = localize_list(
            [
                self.LEFT_OPTION_NOT_LOCALIZED, self.RIGHT_OPTION_NOT_LOCALIZED,
                self.SELECT_OPTION_NOT_LOCALIZED, self.DESELECT_OPTION_NOT_LOCALIZED
            ],
            self.current_language
        )
        if payload in localized_options:
            available_options_count = len(self._available_goals)

            if payload == self.current_localize(self.LEFT_OPTION_NOT_LOCALIZED):
                if self.currently_selected_index > 0:
                    self.currently_selected_index -= 1
            elif payload == self.current_localize(self.RIGHT_OPTION_NOT_LOCALIZED):
                if self.currently_selected_index < available_options_count - 1:
                    self.currently_selected_index += 1
            elif payload == self.current_localize(self.SELECT_OPTION_NOT_LOCALIZED):
                self.selected_goal_ids.add(self._available_goals[self.currently_selected_index].id)
            elif payload == self.current_localize(self.DESELECT_OPTION_NOT_LOCALIZED):
                if self._available_goals[self.currently_selected_index].id in self.selected_goal_ids:
                    self.selected_goal_ids.remove(self._available_goals[self.currently_selected_index].id)

            new_message_text_not_localized = self._create_goal_selector_message_text_not_localized(
                selected_goals=GoalSettingState._selected_goals(self.selected_goal_ids, self._available_goals),
                currently_shown_goal=self._available_goals[self.currently_selected_index]
            )

            await self.messaging_platform.notify_quick_reply_received(chat_quick_reply.message_id)
            await self.messaging_platform.edit_message(
                chat_quick_reply.sender_id,
                chat_quick_reply.quick_reply_about_msg_id,
                self.current_localize(new_message_text_not_localized),
                quick_reply_menu_obj=GoalSettingState._generate_quick_reply_options_menu(
                    self, self._available_goals, self.current_language,
                    self.selected_goal_ids, self.currently_selected_index
                )
            )
        else:
            await super().handle_quick_reply(chat_quick_reply)

    @staticmethod
    def _selected_goals(currently_selected_goal_ids: Collection[str],
                        available_goals: List[AbstractUserGoal]) -> List[AbstractUserGoal]:
        """Utility function to extract currently selected goals"""

        return [goal for goal in available_goals if goal.id in currently_selected_goal_ids]

    @staticmethod
    def _create_goal_selector_message_text_not_localized(
            selected_goals: List[AbstractUserGoal],
            currently_shown_goal: AbstractUserGoal
    ) -> Mapping[Language, str]:
        """Creates the goal selector message string, not localized"""

        result_mapping = {}
        for language in Language:
            currently_shown_goal_text_localized = markup_text(
                localize(currently_shown_goal.text_not_localized, language),
                bold=True
            )
            if not selected_goals:
                result_mapping[language] = currently_shown_goal_text_localized
            else:
                result_mapping[language] = (
                    f"{localize(GoalSettingState.render_goals_not_localized(selected_goals, italic=True), language)}"
                    f"\n\n\n"
                    f"{currently_shown_goal_text_localized}"
                )

        return result_mapping

    @staticmethod
    def render_goals_not_localized(
            goals: List[AbstractUserGoal],
            bold: bool = False,
            italic: bool = False
    ) -> Mapping[Language, str]:
        """Create the string containing the provided goals description, not localized"""

        return {
            language: "- " + "\n\n- ".join([
                markup_text(localize(goal.text_not_localized, language), bold, italic) for goal in goals
            ])
            for language in Language
        }

    @staticmethod
    async def ask_for_goals(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                            current_language: Optional[Language],
                            available_goals: List[AbstractUserGoal],
                            selected_goal_ids: Collection[str] = (), starting_goal_index: int = 0) -> ChatMessage:
        """Utility method to ask for setting user goals"""

        current_state.set_next_state(GoalSettingState.STATE_NAME)
        starting_goal = available_goals[starting_goal_index]
        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            localize(GOALS_QUESTION_TEXT_NOT_LOCALIZED, current_language),
            custom_keyboard_obj=(
                current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                    localize_list(GoalSettingState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
                )
            )
        )
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            GoalSettingState._create_goal_selector_message_text_not_localized(
                GoalSettingState._selected_goals(selected_goal_ids, available_goals),
                starting_goal
            ),
            current_language,
            quick_reply_menu_obj=GoalSettingState._generate_quick_reply_options_menu(
                current_state, available_goals, current_language, selected_goal_ids, starting_goal_index
            )
        )

    @staticmethod
    def _generate_quick_reply_options_menu(current_state: AbstractCovid19ReceiveMessageState,
                                           available_goals: List[AbstractUserGoal],
                                           current_language: Optional[Language],
                                           selected_goal_ids: Collection[str] = (),
                                           starting_goal_index: int = 0) -> Any:
        """Utility method to generate the options menu, according to provided context"""

        starting_goal = available_goals[starting_goal_index]
        not_localized_option_list = (
            GoalSettingState.QUICK_OPTIONS_MENU_NOT_LOCALIZED if starting_goal.id not in selected_goal_ids
            else GoalSettingState.QUICK_OPTIONS_MENU_SELECTED_NOT_LOCALIZED
        )
        return current_state.messaging_platform_handling_strategies.create_quick_menu_from(
            GoalSettingState._slice_first_last_options_if_at_borders(
                element_count=len(available_goals),
                current_index=starting_goal_index,
                option_list=localize_list(not_localized_option_list, current_language)
            )
        )

    @staticmethod
    def _slice_first_last_options_if_at_borders(element_count: int, current_index: int,
                                                option_list: List[str]) -> List[str]:
        """Utility method to slice the options menu, if we are at start or end of data"""
        if element_count == 1:
            return option_list[1:][:-1]  # Remove first and last
        elif element_count > 1:
            if current_index == 0:
                return option_list[1:]  # Remove first
            elif current_index == element_count - 1:
                return option_list[:-1]  # Remove last

        return option_list  # All options to be displayed


class UserEvaluationQuestionsState(AbstractDataInsertionState):
    """The FSM State handling the user evaluation"""

    STATE_NAME = "UserEvaluationQuestionsState"

    PLACE_HOLDER_QUESTION_TEXT_NOT_LOCALIZED = {Language.LANGUAGE_ENGLISH: "Dummy Question"}

    KEYBOARD_OPTIONS_NOT_LOCALIZED = DifficultyField.pretty_values_not_localized()

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_registration_completed: Callable[[AbstractCovid19ReceiveMessageState, str], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):
        super().__init__(UserEvaluationQuestionsState.PLACE_HOLDER_QUESTION_TEXT_NOT_LOCALIZED,
                         UserEvaluationQuestionsState.KEYBOARD_OPTIONS_NOT_LOCALIZED, default_quick_reply_handler,
                         on_registration_completed, get_user_available_goals, get_evaluation_questions,
                         [
                             *GoalSettingState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                             *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         ])

        self.current_displayed_question: Optional[AbstractEvaluationQuestion] = None

    async def on_start(self):
        await super().on_start()

        if self.current_displayed_question is None:
            questions = self._get_evaluation_questions()
            question_with_no_previous = [question for question in questions if question.previous is None]
            self.current_displayed_question: AbstractEvaluationQuestion = question_with_no_previous[0]
            self._question_text_not_localized = self.current_displayed_question.text_not_localized

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        current_question: AbstractEvaluationQuestion = self.current_displayed_question
        difficulty = DifficultyField(DifficultyField.uglify(legal_value))

        if DifficultyField.EASY != difficulty or (
                DifficultyField.EASY == difficulty and current_question.next is None
        ):
            # The user answered that current question is difficult, or there are no more questions
            user.current_question = current_question
            user.current_question_answer = difficulty

            # Cleanup data structures
            self.current_displayed_question: Optional[AbstractEvaluationQuestion] = None
            self._question_text_not_localized = self.PLACE_HOLDER_QUESTION_TEXT_NOT_LOCALIZED

            await self.messaging_platform.send_message_after_sleep(
                sender_id,
                f"{markup_text(self.current_localize(LEVEL_TEXT_NOT_LOCALIZED), italic=True)}: "
                f"{self.compute_user_level(user)}"
            )
            await self.proceed_to_next_state(user, sender_id)
        else:
            self.current_displayed_question = current_question.next
            await self.ask_evaluation_question(self, sender_id, self.current_language, self.current_displayed_question)

    @staticmethod
    async def ask_evaluation_question(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                      current_language: Optional[Language],
                                      to_ask_question: AbstractEvaluationQuestion) -> ChatMessage:
        """Utility method encapsulating the logic to send to the use an evaluation question"""

        current_state.set_next_state(UserEvaluationQuestionsState.STATE_NAME)
        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            to_ask_question.text_not_localized,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(UserEvaluationQuestionsState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            )
        )

    @staticmethod
    async def start_user_evaluation_process(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                            current_language: Optional[Language],
                                            get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                                            ) -> ChatMessage:
        """Utility method to start the user evaluation process"""

        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            localize(LETS_EVALUATE_YOUR_ABILITY_MESSAGE_TEXT, current_language)
        )

        first_question = [question for question in get_evaluation_questions() if question.previous is None][0]

        return await UserEvaluationQuestionsState.ask_evaluation_question(
            current_state, recipient_id, current_language, first_question
        )

    @staticmethod
    def compute_user_level(user: AbstractUser) -> str:
        """Utility method to compute the user level as count of questions from first"""

        return compute_user_level(user.current_question, user.current_question_answer)


class UpdatePersonalDataState(AbstractMenuOptionsHandlingState, AbstractCovid19ReceiveMessageState):
    """The FSM State handling user data updating"""

    STATE_NAME = "UpdatePersonalDataState"

    MODIFY_NAME_OPTION_NOT_LOCALIZED = NAME_TEXT_NOT_LOCALIZED
    MODIFY_LANGUAGE_OPTION_NOT_LOCALIZED = LANGUAGE_TEXT_NOT_LOCALIZED
    MODIFY_SEX_OPTION_NOT_LOCALIZED = SEX_TEXT_NOT_LOCALIZED
    MODIFY_AGE_OPTION_NOT_LOCALIZED = AGE_TEXT_NOT_LOCALIZED
    MODIFY_SPORT_DAYS_OPTION_NOT_LOCALIZED = MODIFY_FAVOURITE_SPORT_DAYS_OPTION_TEXT_NOT_LOCALIZED
    MODIFY_GOALS_OPTION_NOT_LOCALIZED = GOALS_TEXT_NOT_LOCALIZED
    REDO_INITIAL_EVALUATION_NOT_LOCALIZED = REDO_EVALUATION_TEXT_NOT_LOCALIZED

    BACK_TO_MAIN_MENU_OPTION_NOT_LOCALIZED = BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [MODIFY_NAME_OPTION_NOT_LOCALIZED, MODIFY_LANGUAGE_OPTION_NOT_LOCALIZED,
                                      MODIFY_SEX_OPTION_NOT_LOCALIZED, MODIFY_AGE_OPTION_NOT_LOCALIZED,
                                      MODIFY_SPORT_DAYS_OPTION_NOT_LOCALIZED, MODIFY_GOALS_OPTION_NOT_LOCALIZED,
                                      REDO_INITIAL_EVALUATION_NOT_LOCALIZED, BACK_TO_MAIN_MENU_OPTION_NOT_LOCALIZED]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractCovid19ReceiveMessageState, str, bool], Awaitable[None]],
                 get_user_available_goals: Callable[[], List[AbstractUserGoal]],
                 get_evaluation_questions: Callable[[], List[AbstractEvaluationQuestion]],
                 ):

        AbstractMenuOptionsHandlingState.__init__(
            self, WHICH_DATA_TO_UPDATE_QUESTION_TEXT_NOT_LOCALIZED,
            UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
            ignored_messages_not_localized=[
                *NameInsertionState.KEYBOARD_OPTIONS,
                *LanguageInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *SexInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *AgeInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *FavouriteWeekDaysInsertionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *GoalSettingState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *UserEvaluationQuestionsState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *UserFunctionality.pretty_values_not_localized()
            ]
        )
        AbstractCovid19ReceiveMessageState.__init__(self)

        self._default_quick_reply_handler = default_quick_reply_handler
        self._on_back_to_menu_with_optional_message = on_back_to_menu
        self._get_user_available_goals = get_user_available_goals
        self._get_evaluation_questions = get_evaluation_questions

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        language = user.language
        if legal_value == self.current_localize(UpdatePersonalDataState.BACK_TO_MAIN_MENU_OPTION_NOT_LOCALIZED):
            await self._on_back_to_menu_with_optional_message(self, sender_id, True)
        elif legal_value == self.current_localize(UpdatePersonalDataState.MODIFY_LANGUAGE_OPTION_NOT_LOCALIZED):
            await LanguageInsertionState.ask_for_language(self, sender_id, language)
        elif legal_value == self.current_localize(UpdatePersonalDataState.MODIFY_NAME_OPTION_NOT_LOCALIZED):
            await NameInsertionState.ask_for_name(self, sender_id, language)
        elif legal_value == self.current_localize(UpdatePersonalDataState.MODIFY_SEX_OPTION_NOT_LOCALIZED):
            await SexInsertionState.ask_for_sex(self, sender_id, language)
        elif legal_value == self.current_localize(UpdatePersonalDataState.MODIFY_AGE_OPTION_NOT_LOCALIZED):
            await AgeInsertionState.ask_for_age(self, sender_id, language)
        elif legal_value == self.current_localize(UpdatePersonalDataState.MODIFY_SPORT_DAYS_OPTION_NOT_LOCALIZED):
            await FavouriteWeekDaysInsertionState.ask_for_favourite_sport_days(self, sender_id, language)
        elif legal_value == self.current_localize(UpdatePersonalDataState.MODIFY_GOALS_OPTION_NOT_LOCALIZED):
            await GoalSettingState.ask_for_goals(
                self, sender_id, language,
                self._get_user_available_goals(),
                [goal.id for goal in user.goals]
            )
        elif legal_value == self.current_localize(UpdatePersonalDataState.REDO_INITIAL_EVALUATION_NOT_LOCALIZED):
            await UserEvaluationQuestionsState.start_user_evaluation_process(
                self, sender_id, language, self._get_evaluation_questions
            )
        else:
            log(self.agent, f"Not implemented case!! `{legal_value}` was added to legal values but its not handled!",
                logger, logging.ERROR)

    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        await self._default_quick_reply_handler(self, chat_quick_reply)

    @staticmethod
    async def ask_for_what_to_update(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                     current_user: AbstractUser):
        """Utility method to ask the user for which field to update"""
        current_language = current_user.language

        current_state.set_next_state(UpdatePersonalDataState.STATE_NAME)
        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            UpdatePersonalDataState.create_user_data_string(current_user)
        )

        return await ask_question(
            current_state.messaging_platform,
            recipient_id,
            WHICH_DATA_TO_UPDATE_QUESTION_TEXT_NOT_LOCALIZED,
            current_language,
            current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            )
        )

    @staticmethod
    def create_user_data_string(current_user_data: AbstractUser):
        """Utility method to create a user data representation in string form"""

        language = current_user_data.language

        sex_prettifier = SexField.values_prettifier_localized(language)
        age_prettifier = AgeField.values_prettifier_localized(language)
        language_prettifier = Language.values_prettifier_dictionary()
        weekday_prettifier = WeekDayField.values_prettifier_localized(language)

        return (
            f"{markup_text(localize(NAME_TEXT_NOT_LOCALIZED, language), bold=True)}: "
            f"{current_user_data.first_name}\n\n"

            f"{markup_text(localize(LANGUAGE_TEXT_NOT_LOCALIZED, language), bold=True)}: "
            f"{language_prettifier[current_user_data.language.value]}\n\n"

            f"{markup_text(localize(SEX_TEXT_NOT_LOCALIZED, language), bold=True)}: "
            f"{sex_prettifier[current_user_data.sex.value]}\n\n"

            f"{markup_text(localize(AGE_TEXT_NOT_LOCALIZED, language), bold=True)}: "
            f"{age_prettifier[current_user_data.age.value]}\n\n"

            f"{markup_text(localize(FAVOURITE_SPORT_DAYS_TEXT_NOT_LOCALIZED, language), bold=True)}: "
            f"{', '.join([weekday_prettifier[day.value] for day in current_user_data.favourite_sport_days])}\n\n"

            f"{markup_text(localize(LEVEL_TEXT_NOT_LOCALIZED, language), bold=True)}: "
            f"{UserEvaluationQuestionsState.compute_user_level(current_user_data)}\n\n"

            f"{markup_text(localize(GOALS_TEXT_NOT_LOCALIZED, language), bold=True)}:\n\n"
            f"{localize(GoalSettingState.render_goals_not_localized(current_user_data.goals), language)}"
        )
