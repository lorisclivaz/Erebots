import logging
from typing import Optional, List, Tuple, Callable, Mapping

from common.agent.agents.abstract_user_agent import AbstractUserAgent
from common.agent.agents.interaction_texts import localize, markup_text
from common.agent.behaviour.abstract_fsm_state_behaviours import AbstractWaitForMessageState
from common.agent.behaviour.abstract_user_agent_behaviours import AbstractUserRegistrationCheckingState
from common.agent.behaviour.behaviours import TrySubscriptionToAgentBehaviour, WaitForMessageFSMBehaviour
from common.agent.my_logging import log, log_exception
from common.chat.language_enum import Language
from common.chat.message.types import ChatActualMessage, ChatQuickReply
from common.chat.platform.types import ChatPlatform
from common.custom_chat.client_notification_manager import ClientNotificationManager
from common.database.abstract_suggestion_event import AbstractSuggestionEvent
from common.pryv.api_wrapper import PryvAPI
from common.utils.lists import flatten_list
from covid19.common.agent.agents.interaction_texts import (
    BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED, START_COMMAND_ALREADY_REGISTERED_MESSAGE_TEXT_NOT_LOCALIZED,
    MENU_COMMAND_MESSAGE_TEXT_NOT_LOCALIZED, REGISTRATION_COMPLETED_MESSAGE_TEXT_NOT_LOCALIZED,
    LEVEL_TEXT_NOT_LOCALIZED, HERE_ARE_YOUR_STATISTICS_TEXT_NOT_LOCALIZED,
)
from covid19.common.agent.agents.user.abstract_behaviours import (
    AbstractCovid19ReceiveMessageState
)
from covid19.common.agent.agents.user.asked_to_exercise_state import AskedToExerciseState
from covid19.common.agent.agents.user.data_management_states import (
    ask_for_next_missing_field_or_complete_registration, SexInsertionState, AgeInsertionState,
    FavouriteWeekDaysInsertionState, GoalSettingState, UpdatePersonalDataState, LanguageInsertionState,
    UserEvaluationQuestionsState, PryvAccessAskingState, NameInsertionState
)
from covid19.common.agent.agents.user.mappings_to_exercise_sets_utils import get_exercise_sets_for
from covid19.common.agent.agents.user.privacy_statement import generate_privacy_statement_not_localized
from covid19.common.agent.agents.user.proactive_notification_behaviour import ProactiveNotificationSettingBehaviour
from covid19.common.agent.agents.user.sport_session_management_states import (
    InSportSessionState, DifficultyRatingState, FunnyRatingState, AbortSessionState
)
from covid19.common.agent.available_functionality_enums import SlashCommands, UserFunctionality
from covid19.common.database.connection_manager import AbstractCovid19ConnectionManager
from covid19.common.database.enums import Usefulness
from covid19.common.database.user.daos import (
    AbstractUserDAO, AbstractUserGoalDAO, AbstractEvaluationQuestionDAO,
    AbstractQuestionToExerciseSetMappingDAO
)
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal

logger = logging.getLogger(__name__)


class UserAgent(AbstractUserAgent):
    """The Agent which will manage each system User"""

    def __init__(self, jid, password, my_user_id: str, gateway_agents_jids: List[str], doctor_jid: str,
                 default_platform_and_token: Tuple[ChatPlatform, str],
                 db_connection_manager: AbstractCovid19ConnectionManager):
        super().__init__(jid, password, my_user_id, gateway_agents_jids)

        self.doctor_jid: str = doctor_jid
        self.default_platform_and_token: Tuple[ChatPlatform, str] = default_platform_and_token
        self.db_connection_manager: AbstractCovid19ConnectionManager = db_connection_manager

        self.available_goals: Optional[Mapping[str, AbstractUserGoal]] = None
        self.evaluation_questions: Optional[Mapping[str, AbstractEvaluationQuestion]] = None
        self.question_to_exercise_set_mappings: Optional[Mapping[str, AbstractQuestionToExerciseSetMapping]] = None

    async def retrieve_current_user(self) -> AbstractUser:
        self.db_connection_manager.connect_to_db()
        try:
            user_dao: AbstractUserDAO = self.db_connection_manager.get_user_dao()
            return user_dao.find_by_id(self.user_id)
        except:
            log_exception(self, logger)

        self.db_connection_manager.disconnect_from_db()

    async def setup(self):
        await super().setup()

        self.db_connection_manager.connect_to_db()
        self.load_agent_database_fields()

        self.add_behaviour(TrySubscriptionToAgentBehaviour(period=2, to_subscribe_agent_jid=self.doctor_jid))
        self.add_behaviour(ProactiveNotificationSettingBehaviour(
            notification_hours=[10, 17],
            user=self.user,
            client_notification_manager=ClientNotificationManager.get_instance(
                self.db_connection_manager.get_unread_message_dao()
            )
        ))

        log(self, f"UserAgent started.", logger)

    def load_agent_database_fields(self):
        """Utility function to load database fields"""
        log(self, f"Reload agent database fields, for possible data refresh", logger)

        try:
            user_goal_dao: AbstractUserGoalDAO = self.db_connection_manager.get_user_goal_dao()
            self.available_goals: Mapping[str, AbstractUserGoal] = user_goal_dao.find_by()
        except:
            log_exception(self, logger)
        try:
            evaluation_question_dao: AbstractEvaluationQuestionDAO = (
                self.db_connection_manager.get_evaluation_question_dao()
            )
            self.evaluation_questions: Mapping[str, AbstractEvaluationQuestion] = evaluation_question_dao.find_by()
        except:
            log_exception(self, logger)
        try:
            question_to_exercise_set_mapping_dao: AbstractQuestionToExerciseSetMappingDAO = (
                self.db_connection_manager.get_question_to_exercise_set_mapping_dao()
            )
            self.question_to_exercise_set_mappings: Mapping[str, AbstractQuestionToExerciseSetMapping] = (
                question_to_exercise_set_mapping_dao.find_by()
            )
        except:
            log_exception(self, logger)

    class Covid19MessageFSMHandlingBehaviour(WaitForMessageFSMBehaviour):
        """The FSM behaviour handling the Covid19 project interactions towards users"""

        def configure_fsm(self, initial_wait_for_message_state_creator: Callable[[], AbstractWaitForMessageState]):
            initial_default_state = initial_wait_for_message_state_creator()
            super().configure_fsm(lambda: initial_default_state)

            # Getters used by states to indirectly access, the agent fields
            def get_user_available_goals() -> List[AbstractUserGoal]:
                return list(self.agent.available_goals.values())

            def get_evaluation_questions() -> List[AbstractEvaluationQuestion]:
                return list(self.agent.evaluation_questions.values())

            def get_question_to_exercise_set_mappings() -> List[AbstractQuestionToExerciseSetMapping]:
                return list(self.agent.question_to_exercise_set_mappings.values())

            def get_pryv_api() -> PryvAPI:
                db_connection_manager: AbstractCovid19ConnectionManager = self.agent.db_connection_manager
                return PryvAPI(db_connection_manager.pryv_server_domain)

            pryv_access_asking_state = PryvAccessAskingState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions, get_pryv_api
            )
            language_handling_state = LanguageInsertionState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions
            )
            name_handling_state = NameInsertionState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions
            )
            sex_handling_state = SexInsertionState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions
            )
            age_handling_state = AgeInsertionState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions
            )
            sport_days_handling_state = FavouriteWeekDaysInsertionState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions
            )
            goals_handling_state = GoalSettingState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions
            )
            evaluation_handling_state = UserEvaluationQuestionsState(
                _default_handle_quick_reply, _on_registration_completed, get_user_available_goals,
                get_evaluation_questions
            )

            personal_data_handling_state = UpdatePersonalDataState(
                _default_handle_quick_reply, _on_back_to_menu, get_user_available_goals, get_evaluation_questions
            )

            asked_to_exercise = AskedToExerciseState(
                _default_handle_quick_reply, _on_back_to_menu, get_question_to_exercise_set_mappings
            )
            in_sport_session_state = InSportSessionState(
                _default_handle_quick_reply, _on_back_to_menu
            )
            abort_session_state = AbortSessionState(
                _default_handle_quick_reply, _on_back_to_menu
            )
            ask_for_difficulty_rating = DifficultyRatingState(
                _default_handle_quick_reply, _on_back_to_menu, get_question_to_exercise_set_mappings
            )
            ask_for_fun_rating = FunnyRatingState(
                _default_handle_quick_reply, _on_back_to_menu
            )

            # State addition: data insertion
            all_data_insertion_states = [
                pryv_access_asking_state, language_handling_state, name_handling_state, sex_handling_state,
                age_handling_state, sport_days_handling_state, goals_handling_state, evaluation_handling_state
            ]
            for data_insertion_sate in all_data_insertion_states:
                self.add_state(data_insertion_sate.STATE_NAME, data_insertion_sate)

            # State addition: data modification
            self.add_state(personal_data_handling_state.STATE_NAME, personal_data_handling_state)

            # State addition: ask exercise functionality
            self.add_state(asked_to_exercise.STATE_NAME, asked_to_exercise)
            self.add_state(in_sport_session_state.STATE_NAME, in_sport_session_state)
            self.add_state(abort_session_state.STATE_NAME, abort_session_state)
            self.add_state(ask_for_difficulty_rating.STATE_NAME, ask_for_difficulty_rating)
            self.add_state(ask_for_fun_rating.STATE_NAME, ask_for_fun_rating)

            # Transition addition: data insertion (every state connected to next ones directly)
            self.add_waterfall_transitions_from_list(
                initial_default_state.STATE_NAME,
                [state.STATE_NAME for state in [*all_data_insertion_states, initial_default_state]],
                every_state_self_transition=True,
            )

            # Transition addition: data modification
            self.add_transitions_from_list([
                initial_default_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                language_handling_state.STATE_NAME,
                language_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                name_handling_state.STATE_NAME,
                name_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                sex_handling_state.STATE_NAME,
                sex_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                age_handling_state.STATE_NAME,
                age_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                sport_days_handling_state.STATE_NAME,
                sport_days_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                goals_handling_state.STATE_NAME,
                goals_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                evaluation_handling_state.STATE_NAME,
                evaluation_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                personal_data_handling_state.STATE_NAME,
                initial_default_state.STATE_NAME
            ])

            # Transition addition: ask to exercise functionality
            self.add_transitions_from_list([
                initial_default_state.STATE_NAME,
                asked_to_exercise.STATE_NAME,
                asked_to_exercise.STATE_NAME,
                initial_default_state.STATE_NAME,
            ])
            self.add_transitions_from_list([
                asked_to_exercise.STATE_NAME,
                in_sport_session_state.STATE_NAME,
                ask_for_difficulty_rating.STATE_NAME,
                ask_for_difficulty_rating.STATE_NAME,
                in_sport_session_state.STATE_NAME,
                abort_session_state.STATE_NAME,
                abort_session_state.STATE_NAME,
                in_sport_session_state.STATE_NAME,
                in_sport_session_state.STATE_NAME,
                initial_default_state.STATE_NAME,
            ])
            self.add_transitions_from_list([
                ask_for_difficulty_rating.STATE_NAME,
                ask_for_fun_rating.STATE_NAME,
                ask_for_fun_rating.STATE_NAME,
                initial_default_state.STATE_NAME,
            ])
            self.add_transition(abort_session_state.STATE_NAME, initial_default_state.STATE_NAME)
            self.add_transition(ask_for_difficulty_rating.STATE_NAME, initial_default_state.STATE_NAME)

    class MessagingPlatformReceiveMessageState(
        AbstractCovid19ReceiveMessageState, AbstractUserRegistrationCheckingState
    ):
        """The concrete FSM state making this agent wait for messages to be processed from Messaging platforms"""

        STATE_NAME = "MessagingPlatformReceiveMessageState"

        def __init__(self):
            AbstractCovid19ReceiveMessageState.__init__(self)
            AbstractUserRegistrationCheckingState.__init__(self, [
                *UserEvaluationQuestionsState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *UpdatePersonalDataState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *AskedToExerciseState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *InSportSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *AbortSessionState.KEYBOARD_OPTIONS_NOT_LOCALIZED,
                *FunnyRatingState.KEYBOARD_OPTIONS_NOT_LOCALIZED
            ])

            self.should_send_back_the_menu: Optional[bool] = None

        async def on_start(self):
            await super().on_start()

            self.agent.load_agent_database_fields()

            if self.should_send_back_the_menu is None:
                self.should_send_back_the_menu = True

        async def check_user_completed_registration(self, user: AbstractUser) -> bool:
            connection_manager: AbstractCovid19ConnectionManager = self.agent.db_connection_manager
            if user.pryv_endpoint:
                pryv_access_info = PryvAPI(connection_manager.pryv_server_domain).get_access_info(user.pryv_endpoint)
                if pryv_access_info is None:
                    # Token revoked or something wrong with the user permissions, request Pryv auth again
                    user.pryv_endpoint = None
                    user.registration_completed = False

            if (user.registration_completed is True and (
                    user.pryv_endpoint is None or
                    user.language is None or
                    user.first_name is None or
                    user.sex is None or
                    user.age is None or
                    not user.favourite_sport_days or
                    not user.goals or
                    not user.current_question or
                    not user.current_question_answer
            )):
                log(self.agent, f"Detected missing profile information, triggering registration process again.")
                user.registration_completed = False

            return user.registration_completed

        def bot_introduction_message_text_not_localized(self) -> Mapping[Language, str]:
            return BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED

        async def start_registration_process(self, chat_actual_message: ChatActualMessage):
            await ask_for_next_missing_field_or_complete_registration(
                self, chat_actual_message.sender_id, _on_registration_completed,
                get_user_available_goals=lambda: list(self.agent.available_goals.values()),
                get_evaluation_questions=lambda: list(self.agent.evaluation_questions.values())
            )

        async def dispatch_commands(self, chat_actual_message: ChatActualMessage) -> bool:
            msg_text = chat_actual_message.message_text
            sender_id = chat_actual_message.sender_id

            if msg_text == SlashCommands.START.value:
                await handle_command_start(self, sender_id)
                return True
            elif msg_text == SlashCommands.MENU.value:
                await handle_command_menu(self, sender_id)
                return True
            elif msg_text == SlashCommands.HELP.value:
                await handle_command_help(self, sender_id)
                return True

            elif UserFunctionality.uglify(msg_text) == UserFunctionality.UPDATE_PERSONAL_DATA.value:
                await handle_update_personal_data(self, sender_id)
                return True
            elif UserFunctionality.uglify(msg_text) == UserFunctionality.LETS_EXERCISE.value:
                await handle_asked_to_exercise(self, sender_id)
                return True
            elif UserFunctionality.uglify(msg_text) == UserFunctionality.TREND.value:
                await handle_send_statistics(self, sender_id)
                return True
            elif UserFunctionality.uglify(msg_text) == UserFunctionality.PRIVACY_STATEMENT.value:
                await handle_send_privacy_statement(self, sender_id)
                return True
            else:
                return False

        async def handle_ignored_message(self, chat_actual_message: ChatActualMessage):
            if self.should_send_back_the_menu:
                log(self.agent, f"But send back the main menu, to make possible continue the interaction", logger)
                await handle_command_menu(self, chat_actual_message.sender_id)
                self.should_send_back_the_menu = False

        async def send_help_string(self, chat_actual_message: ChatActualMessage):
            await self.messaging_platform.send_message_after_sleep(
                chat_actual_message.sender_id,
                localize(SlashCommands.create_help_string_not_localized(), self.user.language),
                custom_keyboard_obj=self.messaging_platform_handling_strategies.create_main_menu_keyboard(
                    language=self.user.language
                )
            )

        async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
            await _default_handle_quick_reply(self, chat_quick_reply)

    def create_messaging_platform_receive_message_behaviour(self) -> WaitForMessageFSMBehaviour:
        return UserAgent.Covid19MessageFSMHandlingBehaviour(UserAgent.MessagingPlatformReceiveMessageState)


async def handle_command_start(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """The handler function for what should happen when the user sends '/start' command"""
    user, language = _get_user_and_language(state)

    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        localize(START_COMMAND_ALREADY_REGISTERED_MESSAGE_TEXT_NOT_LOCALIZED, language),
        custom_keyboard_obj=state.messaging_platform_handling_strategies.create_main_menu_keyboard(
            language=language
        )
    )


async def handle_command_menu(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """The handler function for what should happen when the user sends '/menu' command"""
    user, language = _get_user_and_language(state)

    await state.messaging_platform.send_message(
        recipient_id,
        localize(MENU_COMMAND_MESSAGE_TEXT_NOT_LOCALIZED, language),
        custom_keyboard_obj=state.messaging_platform_handling_strategies.create_main_menu_keyboard(
            language=language
        )
    )


async def handle_command_help(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """The handler function for what should happen when the user sends '/help' command"""
    user, language = _get_user_and_language(state)

    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        localize(SlashCommands.create_help_string_not_localized(), language)
    )


async def handle_update_personal_data(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """The handler function to handle user request to see/update its data"""
    user, language = _get_user_and_language(state)

    state.should_send_back_the_menu = None  # When going in other menu states this should be reset to None
    await UpdatePersonalDataState.ask_for_what_to_update(state, recipient_id, user)


async def handle_asked_to_exercise(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """The handler function called when the user asks do exercise"""
    user, language = _get_user_and_language(state)

    suitable_exercise_sets = get_exercise_sets_for(
        user, list(state.agent.question_to_exercise_set_mappings.values())
    )
    first_exercise_set = suitable_exercise_sets[0] if suitable_exercise_sets else None

    state.should_send_back_the_menu = None  # When going in other menu states this should be reset to None
    await AskedToExerciseState.handle_user_asked_to_exercise(
        state, recipient_id, first_exercise_set, language,
        other_sets=len(suitable_exercise_sets) > 1
    )


async def handle_send_statistics(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """The handler function called when the user asks its statistics"""
    user, language = _get_user_and_language(state)

    statistic_message_localized = (
        f"{localize(HERE_ARE_YOUR_STATISTICS_TEXT_NOT_LOCALIZED, language)}\n\n"
        f"{markup_text(localize(LEVEL_TEXT_NOT_LOCALIZED, language), bold=True)}: "
        f"{UserEvaluationQuestionsState.compute_user_level(user)}"
    )

    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        statistic_message_localized,
        sleep_seconds=1
    )


async def handle_send_privacy_statement(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """The handler function called when the user asks for the privacy statement"""
    user, language = _get_user_and_language(state)

    privacy_statement_message_localized = localize(generate_privacy_statement_not_localized(), language)

    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        privacy_statement_message_localized,
        sleep_seconds=1
    )


async def _on_registration_completed(state: AbstractCovid19ReceiveMessageState, recipient_id: str):
    """Callback method specifying what should happen on registration completion"""
    user, language = _get_user_and_language(state)

    state.set_next_state(UserAgent.MessagingPlatformReceiveMessageState.STATE_NAME)
    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        localize(REGISTRATION_COMPLETED_MESSAGE_TEXT_NOT_LOCALIZED, language)
    )
    await handle_command_menu(state, recipient_id)


async def _on_back_to_menu(state: AbstractCovid19ReceiveMessageState, recipient_id: str, show_message: bool = True):
    """The callback called when inside a state, the "back to menu" option is pressed"""

    state.set_next_state(UserAgent.MessagingPlatformReceiveMessageState.STATE_NAME)
    if show_message:
        await handle_command_menu(state, recipient_id)


async def _default_handle_quick_reply(state: AbstractCovid19ReceiveMessageState, quick_reply: ChatQuickReply):
    """Default handling "behaviour" to be used in every agent state, to handle quick replies"""

    quick_reply_payload = quick_reply.quick_reply_payload
    log(state.agent, f"Will handle quick reply payload `{quick_reply_payload}` from `{quick_reply.chat_platform}`",
        logger)

    # Removes the inline keyboard which made this callback handler to run
    await state.messaging_platform.edit_quick_replies_for_message_id(
        quick_reply.sender_id,
        quick_reply.quick_reply_about_msg_id
    )

    # If the user changes the language after having received a message in another language, it could be possible to
    # receive a feedback in another language, and it should be treated as valid anyway
    all_pretty_values = flatten_list(
        [list(mapping.values()) for mapping in Usefulness.pretty_values_not_localized()]
    )
    if quick_reply_payload in all_pretty_values:
        await handle_usefulness_feedback(state, quick_reply)
    else:
        log(state.agent,
            f"Unrecognized quick reply payload: `{quick_reply_payload}`. Maybe a not implemented feature!!!",
            logger, logging.WARNING)


async def handle_usefulness_feedback(state: AbstractCovid19ReceiveMessageState, chat_quick_reply: ChatQuickReply):
    """The handler function for usefulness feedback, from the user over sent suggestions"""
    user, language = _get_user_and_language(state)

    feedback = chat_quick_reply.quick_reply_payload

    log(state.agent,
        f"Feedback for message with message_id `{chat_quick_reply.quick_reply_about_msg_id}` "
        f"was `{feedback} ({Usefulness.uglify(feedback)})`", logger)

    found_suggestion_event = _retrieve_sent_suggestion(user, str(chat_quick_reply.quick_reply_about_msg_id))
    if found_suggestion_event:
        found_suggestion_event.suggestion_usefulness = Usefulness.uglify(feedback)

        log(state.agent, f"Feedback saved.", logger)
    else:
        log(state.agent, f"Not found event corresponding to `{chat_quick_reply.quick_reply_about_msg_id}`", logger,
            logging.WARNING)


def _retrieve_sent_suggestion(
        user: AbstractUser,
        to_be_found_message_id: str
) -> Optional[AbstractSuggestionEvent]:
    """A function to retrieve the event bound to the suggestion which the user evaluated"""

    # Implement here the suggestion retrieval

    return None


def _get_user_and_language(state: AbstractCovid19ReceiveMessageState) -> Tuple[AbstractUser, Language]:
    """Utility to extract user and its language from state"""
    return state.user, state.user.language
