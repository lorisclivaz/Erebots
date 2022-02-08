import logging
from typing import Optional, List, Tuple, Callable, Mapping

from common.agent.agents.abstract_user_agent import AbstractUserAgent
from common.agent.agents.interaction_texts import localize
from common.agent.behaviour.abstract_fsm_state_behaviours import AbstractWaitForMessageState
from common.agent.behaviour.abstract_user_agent_behaviours import AbstractUserRegistrationCheckingState
from common.agent.behaviour.behaviours import TrySubscriptionToAgentBehaviour, WaitForMessageFSMBehaviour
from common.agent.my_logging import log, log_exception
from common.chat.language_enum import Language
from common.chat.message.types import ChatActualMessage, ChatQuickReply
from common.chat.platform.types import ChatPlatform
from common.pryv.api_wrapper import PryvAPI
from echo.common.agent.agents.interaction_texts import (
    BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED, START_COMMAND_ALREADY_REGISTERED_MESSAGE_TEXT_NOT_LOCALIZED,
    MENU_COMMAND_MESSAGE_TEXT_NOT_LOCALIZED, REGISTRATION_COMPLETED_MESSAGE_TEXT_NOT_LOCALIZED
)
from echo.common.agent.agents.user.abstract_behaviours import (
    AbstractEchoReceiveMessageState
)
from echo.common.agent.agents.user.data_management_states import (
    ask_for_next_missing_field_or_complete_registration, PryvAccessAskingState, LanguageInsertionState, EchoState
)
from echo.common.agent.agents.user.privacy_statement import generate_privacy_statement_not_localized
from echo.common.agent.available_functionality_enums import SlashCommands, UserFunctionality
from echo.common.database.connection_manager import AbstractEchoConnectionManager
from echo.common.database.user.daos import AbstractUserDAO
from echo.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class UserAgent(AbstractUserAgent):
    """The Agent which will manage each system User"""

    def __init__(self, jid, password, my_user_id: str, gateway_agents_jids: List[str], doctor_jid: str,
                 default_platform_and_token: Tuple[ChatPlatform, str],
                 db_connection_manager: AbstractEchoConnectionManager):
        super().__init__(jid, password, my_user_id, gateway_agents_jids)

        self.doctor_jid: str = doctor_jid
        self.default_platform_and_token: Tuple[ChatPlatform, str] = default_platform_and_token
        self.db_connection_manager: AbstractEchoConnectionManager = db_connection_manager

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

        log(self, f"UserAgent started.", logger)

    def load_agent_database_fields(self):
        """Utility function to load database fields"""
        log(self, f"Reload agent database fields, for possible data refresh", logger)

    class EchoMessageFSMHandlingBehaviour(WaitForMessageFSMBehaviour):
        """The FSM behaviour handling the echo project interactions towards users"""

        def configure_fsm(self, initial_wait_for_message_state_creator: Callable[[], AbstractWaitForMessageState]):
            initial_default_state = initial_wait_for_message_state_creator()
            super().configure_fsm(lambda: initial_default_state)

            # Getters used by states to indirectly access, the agent fields
            def get_pryv_api() -> PryvAPI:
                db_connection_manager: AbstractEchoConnectionManager = self.agent.db_connection_manager
                return PryvAPI(db_connection_manager.pryv_server_domain)

            pryv_access_asking_state = PryvAccessAskingState(
                _default_handle_quick_reply, _on_registration_completed, get_pryv_api
            )
            language_handling_state = LanguageInsertionState(
                _default_handle_quick_reply, _on_registration_completed
            )
            echo_handling_state = EchoState(
                _default_handle_quick_reply, _on_back_to_menu
            )

            # State addition: data insertion
            all_data_insertion_states = [
                pryv_access_asking_state, language_handling_state, echo_handling_state
            ]
            for data_insertion_sate in all_data_insertion_states:
                self.add_state(data_insertion_sate.STATE_NAME, data_insertion_sate)

            # Transition addition: data insertion (every state connected to next ones directly)
            self.add_waterfall_transitions_from_list(
                initial_default_state.STATE_NAME,
                [state.STATE_NAME for state in [*all_data_insertion_states, initial_default_state]],
                every_state_self_transition=True,
            )

    class MessagingPlatformReceiveMessageState(
        AbstractEchoReceiveMessageState, AbstractUserRegistrationCheckingState
    ):
        """The concrete FSM state making this agent wait for messages to be processed from Messaging platforms"""

        STATE_NAME = "MessagingPlatformReceiveMessageState"

        def __init__(self):
            AbstractEchoReceiveMessageState.__init__(self)
            AbstractUserRegistrationCheckingState.__init__(self, [])

            self.should_send_back_the_menu: Optional[bool] = None

        async def on_start(self):
            await super().on_start()

            self.agent.load_agent_database_fields()

            if self.should_send_back_the_menu is None:
                self.should_send_back_the_menu = True

        async def check_user_completed_registration(self, user: AbstractUser) -> bool:
            connection_manager: AbstractEchoConnectionManager = self.agent.db_connection_manager
            if user.pryv_endpoint:
                pryv_access_info = PryvAPI(connection_manager.pryv_server_domain).get_access_info(user.pryv_endpoint)
                if pryv_access_info is None:
                    # Token revoked or something wrong with the user permissions, request Pryv auth again
                    user.pryv_endpoint = None
                    user.registration_completed = False

            if (user.registration_completed is True and (
                    user.pryv_endpoint is None or
                    user.language is None
            )):
                log(self.agent, f"Detected missing profile information, triggering registration process again.")
                user.registration_completed = False

            return user.registration_completed

        def bot_introduction_message_text_not_localized(self) -> Mapping[Language, str]:
            return BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED

        async def start_registration_process(self, chat_actual_message: ChatActualMessage):
            await ask_for_next_missing_field_or_complete_registration(
                self, chat_actual_message.sender_id, _on_registration_completed
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
            elif UserFunctionality.uglify(msg_text) == UserFunctionality.PRIVACY_STATEMENT.value:
                await handle_send_privacy_statement(self, sender_id)
                return True
            elif UserFunctionality.uglify(msg_text) == UserFunctionality.ECHO.value:
                await handle_echo(self, sender_id)
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
        return UserAgent.EchoMessageFSMHandlingBehaviour(UserAgent.MessagingPlatformReceiveMessageState)


async def handle_command_start(state: AbstractEchoReceiveMessageState, recipient_id: str):
    """The handler function for what should happen when the user sends '/start' command"""
    user, language = _get_user_and_language(state)

    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        localize(START_COMMAND_ALREADY_REGISTERED_MESSAGE_TEXT_NOT_LOCALIZED, language),
        custom_keyboard_obj=state.messaging_platform_handling_strategies.create_main_menu_keyboard(
            language=language
        )
    )


async def handle_command_menu(state: AbstractEchoReceiveMessageState, recipient_id: str):
    """The handler function for what should happen when the user sends '/menu' command"""
    user, language = _get_user_and_language(state)

    await state.messaging_platform.send_message(
        recipient_id,
        localize(MENU_COMMAND_MESSAGE_TEXT_NOT_LOCALIZED, language),
        custom_keyboard_obj=state.messaging_platform_handling_strategies.create_main_menu_keyboard(
            language=language
        )
    )


async def handle_command_help(state: AbstractEchoReceiveMessageState, recipient_id: str):
    """The handler function for what should happen when the user sends '/help' command"""
    user, language = _get_user_and_language(state)

    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        localize(SlashCommands.create_help_string_not_localized(), language)
    )


async def handle_send_privacy_statement(state: AbstractEchoReceiveMessageState, recipient_id: str):
    """The handler function called when the user asks for the privacy statement"""
    user, language = _get_user_and_language(state)

    privacy_statement_message_localized = localize(
        generate_privacy_statement_not_localized(state.platform_type), language
    )

    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        privacy_statement_message_localized,
        sleep_seconds=1
    )


async def handle_echo(state: AbstractEchoReceiveMessageState, recipient_id: str):
    """The handler function to handle user request to see/update its data"""
    user, language = _get_user_and_language(state)

    state.should_send_back_the_menu = None  # When going in other menu states this should be reset to None
    await EchoState.start_echo(state, recipient_id, language)


async def _on_registration_completed(state: AbstractEchoReceiveMessageState, recipient_id: str):
    """Callback method specifying what should happen on registration completion"""
    user, language = _get_user_and_language(state)

    state.set_next_state(UserAgent.MessagingPlatformReceiveMessageState.STATE_NAME)
    await state.messaging_platform.send_message_after_sleep(
        recipient_id,
        localize(REGISTRATION_COMPLETED_MESSAGE_TEXT_NOT_LOCALIZED, language)
    )
    await handle_command_menu(state, recipient_id)


async def _on_back_to_menu(state: AbstractEchoReceiveMessageState, recipient_id: str, show_message: bool = True):
    """The callback called when inside a state, the "back to menu" option is pressed"""

    state.set_next_state(UserAgent.MessagingPlatformReceiveMessageState.STATE_NAME)
    if show_message:
        await handle_command_menu(state, recipient_id)


async def _default_handle_quick_reply(state: AbstractEchoReceiveMessageState, quick_reply: ChatQuickReply):
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
    log(state.agent,
        f"Unrecognized quick reply payload: `{quick_reply_payload}`. Maybe a not implemented feature!!!",
        logger, logging.WARNING)


def _get_user_and_language(state: AbstractEchoReceiveMessageState) -> Tuple[AbstractUser, Language]:
    """Utility to extract user and its language from state"""
    return state.user, state.user.language
