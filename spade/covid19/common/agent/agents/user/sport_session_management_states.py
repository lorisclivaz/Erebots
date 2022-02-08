import logging
from abc import ABC
from datetime import datetime
from os import path
from typing import Callable, Awaitable, List, Optional, Mapping, Any

import requests
from aiogram.utils.exceptions import RetryAfter

from common.agent.agents.interaction_texts import localize, localize_list, markup_text
from common.agent.behaviour.abstract_user_agent_behaviours import AbstractMenuOptionsHandlingState
from common.agent.my_logging import log
from common.chat.language_enum import Language
from common.chat.message.types import ChatQuickReply, ChatActualMessage
from common.chat.platform.abstract_messaging_platform import ChatAction
from covid19.common.agent.agents.interaction_texts import (
    IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED, ABORT_SPORT_SESSION_TEXT_NOT_LOCALIZED,
    TELL_ME_WHEN_FINISHED_TEXT_NOT_LOCALIZED, HOW_MUCH_DIFFICULT_QUESTION_TEXT_NOT_LOCALIZED,
    HERE_IT_IS_THE_NEXT_EXERCISE_TEXT_NOT_LOCALIZED, DID_YOU_HAVE_FUN_QUESTION_TEXT_NOT_LOCALIZED,
    GOOD_JOB_HERES_THE_SESSION_SUMMARY_TEXT_NOT_LOCALIZED, DURATION_TEXT_NOT_LOCALIZED, LEVEL_TEXT_NOT_LOCALIZED,
    YOUR_RATING_TEXT_NOT_LOCALIZED, NEW_LEVEL_REACHED_TEXT_NOT_LOCALIZED, START_NOW_BUTTON_TEXT_NOT_LOCALIZED,
    BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED, YES_BUTTON_TEXT_NOT_LOCALIZED,
    ARE_YOU_SURE_TO_ABORT_SESSION_TEXT_NOT_LOCALIZED, bot_cool_down_message_text_not_localized,
    TOO_DIFFICULT_TRY_WITH_EASIER_EXERCISES_MESSAGE_TEXT_NOT_LOCALIZED
)
from covid19.common.agent.agents.user.abstract_behaviours import (
    AbstractCovid19ReceiveMessageState
)
from covid19.common.agent.agents.user.data_management_states import UserEvaluationQuestionsState
from covid19.common.agent.agents.user.mappings_to_exercise_sets_utils import shift_question_or_difficulty
from covid19.common.database.user.factory import DoneExerciseFactory
from covid19.common.database.user.field_enums import DifficultyField, FunnyField, ShiftField
from covid19.common.database.user.model.abstract_exercise import AbstractExercise
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


def get_exercise_gif_path(exercise: AbstractExercise, internal_address: bool = False) -> str:
    """Extracts the gif path to be sent to the user"""

    from common.agent.web.server_address import WEB_SERVER_INTERNAL_IP, WEB_SERVER_INTERNAL_PORT
    from common.agent.web.server_address import WEB_SERVER_PUBLIC_IP, WEB_SERVER_PUBLIC_PORT
    from covid19.common.agent.agents.doctor.web_api_controllers import API_MOUNT_POINT

    if internal_address:
        web_address = WEB_SERVER_INTERNAL_IP
        web_port = WEB_SERVER_INTERNAL_PORT
    else:
        web_address = WEB_SERVER_PUBLIC_IP
        web_port = WEB_SERVER_PUBLIC_PORT

    if web_address == "localhost" or web_address == WEB_SERVER_INTERNAL_IP or web_address.startswith("192.168."):
        protocol = "http"
    else:
        protocol = "https"

    return f"{protocol}://{web_address}:{web_port}{API_MOUNT_POINT}/exercise/{exercise.id}/gif"


def check_existence(path_or_link: str) -> bool:
    """Utility method to check if a path/link exists/is reachable"""
    return path_or_link and (
            path.exists(path_or_link) or (path_or_link.startswith("http") and
                                          requests.head(path_or_link).status_code == 200)
    )


def is_user_tracking_a_sport_session(user: AbstractUser):
    """Utility method to know if a user has an ongoing sport session tracking"""

    return user.sport_sessions[-1].ended_at is None if user.sport_sessions else False


def get_next_not_done_exercise(current_session: AbstractSportSession) -> Optional[AbstractExercise]:
    """Utility method to get the next to be done exercise"""

    for to_do_exercise in current_session.exercise_set.exercise_list:
        if to_do_exercise.id not in [
            done_exercise.exercise.id
            for done_exercise in current_session.done_exercises_ordered
        ]:
            return to_do_exercise

    return None


class AbstractSessionManagementState(AbstractMenuOptionsHandlingState, AbstractCovid19ReceiveMessageState, ABC):
    """An abstract base class for session management states"""

    STATE_NAME = "AbstractSessionManagementState"

    def __init__(self, question_text_not_localized: Mapping[Language, str],
                 available_options_not_localized: List[Mapping[Language, str]],
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractCovid19ReceiveMessageState, str, bool], Awaitable[None]],
                 ignored_messages_not_localized: List[Mapping[Language, str]],
                 ):
        AbstractMenuOptionsHandlingState.__init__(
            self, question_text_not_localized, available_options_not_localized, ignored_messages_not_localized
        )
        AbstractCovid19ReceiveMessageState.__init__(self)

        self._default_quick_reply_handler = default_quick_reply_handler
        self._on_back_to_menu_with_optional_message = on_back_to_menu

        self.current_session: Optional[AbstractSportSession] = None

    async def on_start(self):
        await super().on_start()
        # NOTE: this gets called every time the user clicks something

        if self.current_session is None:
            self.current_session = self.user.sport_sessions[-1]

    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        await self._default_quick_reply_handler(self, chat_quick_reply)


class InSportSessionState(AbstractSessionManagementState):
    """The state managing the behaviour during a sport session"""

    STATE_NAME = "InSportSessionState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [
        IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED,
        ABORT_SPORT_SESSION_TEXT_NOT_LOCALIZED
    ]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractCovid19ReceiveMessageState, str, bool], Awaitable[None]]
                 ):
        super().__init__(TELL_ME_WHEN_FINISHED_TEXT_NOT_LOCALIZED, InSportSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         default_quick_reply_handler, on_back_to_menu, [
                             START_NOW_BUTTON_TEXT_NOT_LOCALIZED,
                             BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED,
                             *DifficultyRatingState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                             *AbortSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                         ])

        self.current_exercise: Optional[AbstractExercise] = None
        self.exercise_start_datetime: Optional[datetime] = None

    async def on_start(self):
        await super().on_start()
        # NOTE: this gets called every time the user clicks something

        if self.current_exercise is None:
            self.current_exercise = get_next_not_done_exercise(self.current_session)
            self.exercise_start_datetime = (
                self.current_session.done_exercises_ordered[-1].ended_at
                if len(self.current_session.done_exercises_ordered) > 0
                else self.current_session.started_at
            )
            self.exercise_start_datetime = self.exercise_start_datetime.replace(tzinfo=None)

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        if legal_value == self.current_localize(IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED):
            new_done_exercise = DoneExerciseFactory.new_done_exercise(self.current_exercise, datetime.now())
            self.current_session.append_done_exercise(new_done_exercise)

            await DifficultyRatingState.ask_for_difficulty_rating(self, sender_id, self.current_language)
        elif legal_value == self.current_localize(ABORT_SPORT_SESSION_TEXT_NOT_LOCALIZED):
            await AbortSessionState.ask_if_sure_to_abort_session(self, sender_id, self.current_language)
        else:
            log(self.agent,
                f"Not implemented case!! `{legal_value}` was added to legal values but its not handled!",
                logger, logging.ERROR)

        # Cleanup data structures
        self.current_session: Optional[AbstractSportSession] = None
        self.current_exercise: Optional[AbstractExercise] = None
        self.exercise_start_datetime: Optional[datetime] = None

    @staticmethod
    async def enter_sport_session_with_exercise(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                                current_language: Optional[Language], exercise: AbstractExercise):
        """Utility method to send the user single exercises of the sport session"""

        await current_state.messaging_platform.send_chat_action(recipient_id, ChatAction.UPLOAD_PHOTO)
        await InSportSessionState.send_exercise_message(
            current_state, recipient_id, exercise, current_language
        )

        await InSportSessionState.ask_user_when_finished(current_state, recipient_id, current_language)

    @staticmethod
    async def ask_user_when_finished(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                     current_language: Optional[Language]):
        """Utility method to send the user the message and keyboard to advance exercise (or abort session)"""

        current_state.set_next_state(InSportSessionState.STATE_NAME)
        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            localize(TELL_ME_WHEN_FINISHED_TEXT_NOT_LOCALIZED, current_language),
            custom_keyboard_obj=(
                current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                    localize_list(InSportSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
                )
            ),
            sleep_seconds=2.5
        )

    @staticmethod
    async def send_exercise_message(current_state: AbstractCovid19ReceiveMessageState,
                                    recipient_id: str, exercise: AbstractExercise, current_language: Optional[Language],
                                    menu_keyboard_object: Optional[Any] = None):
        """Utility method to send a single exercise message"""

        async def send_exercise_as_text():
            """Method containing the backup strategy to send the exercise message, as text"""

            await current_state.messaging_platform.send_message(
                recipient_id,
                f"{localize(exercise.text_not_localized, current_language)}",
                custom_keyboard_obj=menu_keyboard_object
            )

        if check_existence(get_exercise_gif_path(exercise, internal_address=True)):
            # We have a gif to send with the suggestion
            try:
                await current_state.messaging_platform.send_animation(
                    recipient_id,
                    get_exercise_gif_path(exercise, internal_address=False),
                    image_description=f"{localize(exercise.text_not_localized, current_language)}",
                    custom_keyboard_obj=menu_keyboard_object
                )
            except RetryAfter as exception:
                log(current_state.agent, f"Bot has gone in AntiFloodException. Won't send images for "
                                         f"{exception.timeout} seconds", logger)
                await current_state.messaging_platform.send_message_after_sleep(
                    recipient_id,
                    localize(bot_cool_down_message_text_not_localized(exception.timeout), current_language)
                )
                await send_exercise_as_text()
        else:
            # We don't have a gif to send
            log(current_state.agent,
                f"Current exercise `{exercise.id}` doesn't have a GIF attached, or it has"
                f"but it's not available: `{exercise.gif_path}`. Defaulting to bare text.", logger)
            await send_exercise_as_text()


class AbortSessionState(AbstractSessionManagementState):
    """A FSM State to handle abortion of a sport session"""

    STATE_NAME = "AbortSessionState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [
        YES_BUTTON_TEXT_NOT_LOCALIZED,
        BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED
    ]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractCovid19ReceiveMessageState, str, bool], Awaitable[None]]
                 ):
        super().__init__(ARE_YOU_SURE_TO_ABORT_SESSION_TEXT_NOT_LOCALIZED,
                         AbortSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED, default_quick_reply_handler, on_back_to_menu,
                         [
                             *InSportSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED
                         ])

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        if legal_value == self.current_localize(YES_BUTTON_TEXT_NOT_LOCALIZED):
            self.abort_sport_session(self.current_session)

            await self._on_back_to_menu_with_optional_message(self, sender_id, True)
        elif legal_value == self.current_localize(BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED):
            await InSportSessionState.ask_user_when_finished(self, sender_id, self.current_language)
        else:
            log(self.agent,
                f"Not implemented case!! `{legal_value}` was added to legal values but its not handled!",
                logger, logging.ERROR)

        # Cleanup data structures
        self.current_session: Optional[AbstractSportSession] = None

    @staticmethod
    async def ask_if_sure_to_abort_session(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                           current_language: Optional[Language]):
        """Utility method to ask the user if wants to really abort the sport session"""

        current_state.set_next_state(AbortSessionState.STATE_NAME)

        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            localize(ARE_YOU_SURE_TO_ABORT_SESSION_TEXT_NOT_LOCALIZED, current_language),
            custom_keyboard_obj=(
                current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                    localize_list(AbortSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
                )
            )
        )

    @staticmethod
    def abort_sport_session(to_abort_session: AbstractSportSession):
        """Utility method to abort a sport session"""
        to_abort_session.ended_at = datetime.now()
        to_abort_session.aborted = True


class DifficultyRatingState(AbstractSessionManagementState):
    """A FSM State to handle user difficulty rating for an exercise"""

    STATE_NAME = "DifficultyRatingState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = DifficultyField.pretty_values_not_localized()

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractCovid19ReceiveMessageState, str, bool], Awaitable[None]],
                 get_question_to_exercise_set_mappings: Callable[[], List[AbstractQuestionToExerciseSetMapping]],
                 ):
        super().__init__(HOW_MUCH_DIFFICULT_QUESTION_TEXT_NOT_LOCALIZED,
                         DifficultyRatingState.KEYBOARD_OPTIONS_NOT_LOCALIZED, default_quick_reply_handler,
                         on_back_to_menu, [
                             *InSportSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED
                         ])

        self._get_question_to_exercise_set_mappings = get_question_to_exercise_set_mappings

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        user_difficulty_rating: DifficultyField = DifficultyField(DifficultyField.uglify(legal_value))

        last_exercise = self.current_session.done_exercises_ordered[-1]
        last_exercise.difficulty_rating = user_difficulty_rating

        if len(self.current_session.done_exercises_ordered) == len(self.current_session.exercise_set.exercise_list):
            # Gracefully end sport session
            self.current_session.ended_at = last_exercise.ended_at

            user_level_updated = self.update_user_level(user, self._get_question_to_exercise_set_mappings())
            await self._send_last_sport_session_summary(sender_id, user_level_updated)

            await FunnyRatingState.ask_for_fun_rating(self, sender_id, self.current_language)
        else:
            if user_difficulty_rating in [
                DifficultyField.DIFFICULT,
                DifficultyField.VERY_DIFFICULT,
                DifficultyField.IMPOSSIBLE
            ]:
                # The user found the exercise too difficult, abort current session and downgrade its level
                AbortSessionState.abort_sport_session(self.current_session)
                self.update_user_level(user, self._get_question_to_exercise_set_mappings())
                too_difficult_message_localized = (
                    f"{self.current_localize(TOO_DIFFICULT_TRY_WITH_EASIER_EXERCISES_MESSAGE_TEXT_NOT_LOCALIZED)}\n\n"
                    f"{markup_text(self.current_localize(LEVEL_TEXT_NOT_LOCALIZED), italic=True)}: "
                    f"{UserEvaluationQuestionsState.compute_user_level(user)}"
                )
                await self.messaging_platform.send_message_after_sleep(sender_id, too_difficult_message_localized)
                await self._on_back_to_menu_with_optional_message(self, sender_id, True)
            else:
                await self.messaging_platform.send_message_after_sleep(
                    sender_id,
                    self.current_localize(HERE_IT_IS_THE_NEXT_EXERCISE_TEXT_NOT_LOCALIZED)
                )
                next_exercise = get_next_not_done_exercise(self.current_session)
                await InSportSessionState.enter_sport_session_with_exercise(
                    self, sender_id, self.current_language, next_exercise
                )

        # Cleanup data structures
        self.current_session: Optional[AbstractSportSession] = None

    @staticmethod
    async def ask_for_difficulty_rating(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                        current_language: Optional[Language]):
        """Utility method to ask an exercise difficulty rating"""

        current_state.set_next_state(DifficultyRatingState.STATE_NAME)
        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            localize(HOW_MUCH_DIFFICULT_QUESTION_TEXT_NOT_LOCALIZED, current_language),
            custom_keyboard_obj=current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(DifficultyRatingState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            ),
            sleep_seconds=1.5
        )

    @staticmethod
    def update_user_level(
            user: AbstractUser,
            question_to_exercise_set_mappings: List[AbstractQuestionToExerciseSetMapping]
    ) -> bool:
        """
        Utility method to encapsulate the user level updating logic

        :returns: True if it actually updated user level, False otherwise
        """

        last_session = user.sport_sessions[-1]
        done_exercises_difficulty_rating = [
            done_exercise.difficulty_rating for done_exercise in last_session.done_exercises_ordered
        ]

        to_be_done_shift: Optional[ShiftField] = None

        if set(done_exercises_difficulty_rating).isdisjoint(
                {DifficultyField.DIFFICULT, DifficultyField.VERY_DIFFICULT, DifficultyField.IMPOSSIBLE}
        ):
            # None of the user rating are DIFFICULT, VERY_DIFFICULT, IMPOSSIBLE

            difficulty_ratings = set(done_exercises_difficulty_rating)
            if len(difficulty_ratings) == 1 and DifficultyField.EASY in difficulty_ratings:
                # If Easy is the only rating the user gave to every exercise, lets advance its level

                logger.info(f" Shift the user to next difficulty level.")
                to_be_done_shift = ShiftField.NEXT
            else:
                # Otherwise nothing happens
                logger.info(f" User level unchanged.")
        else:
            # Some of the user ratings were DIFFICULT or harder, lets reduce user level
            logger.info(f" Shift the user to previous difficulty level.")
            to_be_done_shift = ShiftField.PREVIOUS

        if to_be_done_shift is not None:
            new_question, new_difficulty = shift_question_or_difficulty(
                question_to_exercise_set_mappings, user.current_question, user.current_question_answer,
                to_be_done_shift
            )
            logger.info(f" New user level composed by question `{new_question.id}` and difficulty `{new_difficulty}`")
            user.current_question = new_question
            user.current_question_answer = new_difficulty
            return True
        else:
            return False

    async def _send_last_sport_session_summary(self, recipient_id: str, user_level_updated: bool):
        """Utility method to send last sport session summary message to the user"""

        last_sport_session = self.user.sport_sessions[-1]

        last_start_time = last_sport_session.started_at
        difficulty_prettifier = DifficultyField.values_prettifier_not_localized()
        done_exercise_set_text_not_localized = {}
        for index, done_exercise in enumerate(last_sport_session.done_exercises_ordered):
            time_delta = done_exercise.ended_at - last_start_time
            last_start_time = done_exercise.ended_at
            for language, exercise_text in done_exercise.exercise.text_not_localized.items():
                difficulty_rating_not_localized = difficulty_prettifier[done_exercise.difficulty_rating.value]
                done_exercise_set_text_not_localized[language] = (
                    f"{done_exercise_set_text_not_localized.get(language, '')}\n"

                    f"{index + 1}. {markup_text(exercise_text, bold=True)}\n"

                    f"    {markup_text(YOUR_RATING_TEXT_NOT_LOCALIZED[language], italic=True)}: "
                    f"{localize(difficulty_rating_not_localized, language)}\n"

                    f"    {markup_text(DURATION_TEXT_NOT_LOCALIZED[language], italic=True)}: "
                    f"{str(time_delta).split('.')[0]}\n"
                )

        await self.messaging_platform.send_message_after_sleep(
            recipient_id,
            (
                    localize(GOOD_JOB_HERES_THE_SESSION_SUMMARY_TEXT_NOT_LOCALIZED, self.current_language) + '\n\n' +
                    localize(done_exercise_set_text_not_localized, self.current_language) + '\n\n' +
                    (
                        (
                                markup_text(
                                    localize(NEW_LEVEL_REACHED_TEXT_NOT_LOCALIZED, self.current_language),
                                    bold=True
                                ) + '\n'
                        )
                        if user_level_updated else ''
                    ) +
                    markup_text(localize(LEVEL_TEXT_NOT_LOCALIZED, self.current_language), italic=True) + ": " +
                    UserEvaluationQuestionsState.compute_user_level(self.user)
            ),
            sleep_seconds=2
        )


class FunnyRatingState(AbstractSessionManagementState):
    """A FSM State to handle user funny rating for an exercise set"""

    STATE_NAME = "FunnyRatingState"

    KEYBOARD_OPTIONS_NOT_LOCALIZED = FunnyField.pretty_values_not_localized()

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractCovid19ReceiveMessageState, str, bool], Awaitable[None]]
                 ):
        super().__init__(DID_YOU_HAVE_FUN_QUESTION_TEXT_NOT_LOCALIZED,
                         FunnyRatingState.KEYBOARD_OPTIONS_NOT_LOCALIZED, default_quick_reply_handler,
                         on_back_to_menu, [
                             *DifficultyRatingState.KEYBOARD_OPTIONS_NOT_LOCALIZED
                         ])

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        self.current_session.fun_rating = FunnyField(FunnyField.uglify(legal_value))

        await self._on_back_to_menu_with_optional_message(self, sender_id, True)

        # Cleanup data structures
        self.current_session: Optional[AbstractSportSession] = None

    @staticmethod
    async def ask_for_fun_rating(current_state: AbstractCovid19ReceiveMessageState, recipient_id: str,
                                 current_language: Optional[Language]):
        """Utility method to ask an exercise set funny rating"""

        current_state.set_next_state(FunnyRatingState.STATE_NAME)
        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            localize(DID_YOU_HAVE_FUN_QUESTION_TEXT_NOT_LOCALIZED, current_language),
            custom_keyboard_obj=current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                localize_list(FunnyRatingState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
            ),
            sleep_seconds=1.5
        )
