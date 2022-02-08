import logging
from datetime import datetime
from typing import List, Callable, Awaitable, Optional

from common.agent.agents.interaction_texts import localize, SORRY_INTERNAL_ERROR_TEXT_NOT_LOCALIZED, localize_list
from common.agent.behaviour.abstract_user_agent_behaviours import AbstractMenuOptionsHandlingState
from common.agent.my_logging import log
from common.chat.language_enum import Language
from common.chat.message.types import ChatQuickReply, ChatActualMessage
from covid19.common.agent.agents.interaction_texts import (
    START_NOW_BUTTON_TEXT_NOT_LOCALIZED, BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED,
    I_PROPOSE_THIS_EXERCISES_TEXT_NOT_LOCALIZED, HERE_IT_IS_THE_EXERCISE_TEXT_NOT_LOCALIZED,
    CHOOSE_DIFFERENT_EXERCISE_SETS_WITH_ARROWS_TEXT_NOT_LOCALIZED
)
from covid19.common.agent.agents.user.abstract_behaviours import AbstractCovid19ReceiveMessageState
from covid19.common.agent.agents.user.mappings_to_exercise_sets_utils import get_exercise_sets_for
from covid19.common.agent.agents.user.sport_session_management_states import InSportSessionState
from covid19.common.agent.available_functionality_enums import UserFunctionality
from covid19.common.database.user.factory import SportSessionFactory
from covid19.common.database.user.field_enums import ShiftField
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class AskedToExerciseState(AbstractMenuOptionsHandlingState, AbstractCovid19ReceiveMessageState):
    """The state managing a request for an activity suggestion from the user"""

    STATE_NAME = "AskedToExerciseState"

    QUICK_OPTIONS_MENU_NOT_LOCALIZED = ShiftField.pretty_values_not_localized()

    KEYBOARD_OPTIONS_NOT_LOCALIZED = [
        START_NOW_BUTTON_TEXT_NOT_LOCALIZED,
        BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED
    ]

    def __init__(self,
                 default_quick_reply_handler: Callable[
                     [AbstractCovid19ReceiveMessageState, ChatQuickReply], Awaitable[None]
                 ],
                 on_back_to_menu: Callable[[AbstractCovid19ReceiveMessageState, str, bool], Awaitable[None]],
                 get_question_to_exercise_set_mappings: Callable[[], List[AbstractQuestionToExerciseSetMapping]],
                 ):

        AbstractMenuOptionsHandlingState.__init__(self, I_PROPOSE_THIS_EXERCISES_TEXT_NOT_LOCALIZED,
                                                  AskedToExerciseState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                                                  [*UserFunctionality.pretty_values_not_localized()])
        AbstractCovid19ReceiveMessageState.__init__(self)

        self._default_quick_reply_handler = default_quick_reply_handler
        self._on_back_to_menu_with_optional_message = on_back_to_menu
        self._get_question_to_exercise_set_mappings = get_question_to_exercise_set_mappings

        self.suitable_exercise_sets: Optional[List[AbstractExerciseSet]] = None
        self.current_displayed_exercise_set_index: int = 0

    async def on_start(self):
        await super().on_start()
        # NOTE: this gets called every time the user clicks something

        if self.suitable_exercise_sets is None:
            self.suitable_exercise_sets = get_exercise_sets_for(
                self.user, self._get_question_to_exercise_set_mappings()
            )

    async def on_legal_value(self, user: AbstractUser, chat_actual_message: ChatActualMessage):
        legal_value: str = chat_actual_message.message_text
        sender_id: str = chat_actual_message.sender_id
        if legal_value == self.current_localize(BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED):
            await self.delete_sent_exercise_set_messages(sender_id)
            await self._on_back_to_menu_with_optional_message(self, sender_id, True)
        elif legal_value == self.current_localize(START_NOW_BUTTON_TEXT_NOT_LOCALIZED):
            if len(self.suitable_exercise_sets) > 1:
                # Remove quick reply selectors
                await self.messaging_platform.edit_quick_replies_for_message_id(
                    sender_id,
                    self.messaging_platform.last_sent_message.message_id
                )

            current_exercise_set: AbstractExerciseSet = self.suitable_exercise_sets[
                self.current_displayed_exercise_set_index
            ]
            await self.close_ongoing_sport_sessions_if_any()
            new_sport_session = SportSessionFactory.new_sport_session(
                exercise_set=current_exercise_set
            )
            user.append_sport_session(new_sport_session)

            await self.messaging_platform.send_message_after_sleep(
                sender_id,
                self.current_localize(HERE_IT_IS_THE_EXERCISE_TEXT_NOT_LOCALIZED),
                sleep_seconds=0.5
            )
            await InSportSessionState.enter_sport_session_with_exercise(
                self, sender_id, self.current_language, current_exercise_set.exercise_list[0]
            )
        else:
            log(self.agent,
                f"Not implemented case!! `{legal_value}` was added to legal values but its not handled!",
                logger, logging.ERROR)

        # Cleanup data structures
        self.suitable_exercise_sets: Optional[List[AbstractExerciseSet]] = None
        self.current_displayed_exercise_set_index = 0

    async def on_illegal_value(self, chat_actual_message: ChatActualMessage):
        await self.delete_sent_exercise_set_messages(chat_actual_message.sender_id)
        await super().on_illegal_value(chat_actual_message)
        await AskedToExerciseState.handle_user_asked_to_exercise(
            self,
            chat_actual_message.sender_id,
            self.suitable_exercise_sets[self.current_displayed_exercise_set_index],
            self.current_language,
            other_sets=len(self.suitable_exercise_sets) > 1
        )

    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        payload = chat_quick_reply.quick_reply_payload
        exercises_count: int = len(self.suitable_exercise_sets)
        if payload in ShiftField.pretty_values_localized(self.current_language):

            if ShiftField.uglify(payload) == ShiftField.NEXT.value:
                # go forward by one
                self.current_displayed_exercise_set_index = (
                        (self.current_displayed_exercise_set_index + 1) % exercises_count
                )
            else:
                # go back by one
                self.current_displayed_exercise_set_index = (
                        (self.current_displayed_exercise_set_index + (exercises_count - 1)) % exercises_count
                )

            new_suggestion: AbstractExerciseSet = self.suitable_exercise_sets[
                self.current_displayed_exercise_set_index
            ]

            await self.messaging_platform.notify_quick_reply_received(chat_quick_reply.message_id)
            await self.delete_sent_exercise_set_messages(chat_quick_reply.sender_id)
            await self.send_exercises_set_message(
                self, chat_quick_reply.sender_id, new_suggestion, self.current_language,
                other_sets=len(self.suitable_exercise_sets) > 1
            )
        else:
            await self._default_quick_reply_handler(self, chat_quick_reply)

    async def delete_sent_exercise_set_messages(self, sender_id: str):
        """Utility method to delete messages sent by this state, regarding exercise sets"""

        # sent_exercise_in_set_count = len([
        #     exercise for exercise
        #     in self.suitable_exercise_sets[self.current_displayed_exercise_set_index].exercise_list
        #     if check_existence(exercise.gif_path)
        # ])
        # for index in range(sent_exercise_in_set_count):
        #     await self.messaging_platform.delete_message(
        #         sender_id,
        #         self.messaging_platform.sent_messages[-(index + 2)].message_id  # Delete gif messages
        #     )
        await self.messaging_platform.delete_message(
            sender_id,
            self.messaging_platform.last_sent_message.message_id
        )

    async def close_ongoing_sport_sessions_if_any(self):
        """Utility method to close ongoing sport session if any present"""

        user_sessions = self.user.sport_sessions
        for session in user_sessions:
            if session.ended_at is None:
                session.ended_at = datetime.now()
                session.aborted = True

    @staticmethod
    async def handle_user_asked_to_exercise(current_state: AbstractCovid19ReceiveMessageState,
                                            recipient_id: str, exercise_set: Optional[AbstractExerciseSet],
                                            current_language: Optional[Language], other_sets: bool = True):
        """Utility method to send the user a message to suggest the set of exercises"""

        if not exercise_set:
            await current_state.messaging_platform.send_message_after_sleep(
                recipient_id,
                localize(SORRY_INTERNAL_ERROR_TEXT_NOT_LOCALIZED, current_language)
            )
        else:
            current_state.set_next_state(AskedToExerciseState.STATE_NAME)

            await current_state.messaging_platform.send_message_after_sleep(
                recipient_id,
                localize(I_PROPOSE_THIS_EXERCISES_TEXT_NOT_LOCALIZED, current_language),
                custom_keyboard_obj=(
                    current_state.messaging_platform_handling_strategies.create_menu_keyboard_from(
                        localize_list(AskedToExerciseState.KEYBOARD_OPTIONS_NOT_LOCALIZED, current_language)
                    )
                )
            )

            await AskedToExerciseState.send_exercises_set_message(
                current_state, recipient_id, exercise_set, current_language, other_sets
            )

    @staticmethod
    async def send_exercises_set_message(current_state: AbstractCovid19ReceiveMessageState,
                                         recipient_id: str, exercise_set: AbstractExerciseSet,
                                         current_language: Optional[Language], other_sets: bool = True):
        """Utility method to send the exercise set suggestion message"""

        exercise_set_text_not_localized = {}
        for index, exercise in enumerate(exercise_set.exercise_list):
            for language, exercise_text in exercise.text_not_localized.items():
                exercise_set_text_not_localized[language] = (
                    f"{exercise_set_text_not_localized.get(language, '')}\n"
                    f"{index + 1}. {exercise_text}"
                )

        # await current_state.messaging_platform.send_chat_action(recipient_id, ChatAction.UPLOAD_PHOTO)
        # await current_state.messaging_platform.send_media_group(
        #     recipient_id,
        #     {
        #         exercise.gif_path: localize(exercise.text_not_localized, current_language)
        #         for exercise in exercise_set.exercise_list
        #         if check_existence(exercise.gif_path)
        #     }
        # )

        await current_state.messaging_platform.send_message_after_sleep(
            recipient_id,
            f"{localize(exercise_set_text_not_localized, current_language)}" + (
                f"\n\n{localize(CHOOSE_DIFFERENT_EXERCISE_SETS_WITH_ARROWS_TEXT_NOT_LOCALIZED, current_language)}"
                if other_sets else ""
            ),
            quick_reply_menu_obj=current_state.messaging_platform_handling_strategies.create_quick_menu_from(
                localize_list(AskedToExerciseState.QUICK_OPTIONS_MENU_NOT_LOCALIZED, current_language)
            ) if other_sets else None,
            sleep_seconds=1.5
        )
