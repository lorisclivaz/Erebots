import logging
from typing import Any, Optional, Dict

from common.agent.agents.interaction_texts import localize_list
from common.chat.language_enum import Language
from common.chat.message.types import ChatMessage
from common.custom_chat.agent.strategies.chat_platform.custom_chat_handling_strategies_mixin import (
    CustomChatMessageHandlingStrategiesMixin
)
from covid19.common.agent.available_functionality_enums import UserFunctionality
from covid19.common.agent.strategies.chat_platform.abstract_covid19_handling_strategies import (
    AbstractCovid19HandlingStrategies
)
from covid19.common.database.enums import Usefulness
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class CustomChatCovid19HandlingStrategies(AbstractCovid19HandlingStrategies, CustomChatMessageHandlingStrategiesMixin):
    """Concrete strategies for CustomChat messaging platform"""

    def create_inline_menu_from(self, option_dict: Dict[str, str], row_width: int = 3) -> Any:
        pass

    def bind_messaging_platform_id_to_user_id(self, user: AbstractUser, chat_message: ChatMessage):
        if not user.custom_chat_id:
            # Bind user ID to custom chat ID, if not already
            user.custom_chat_id = chat_message.sender_id
            logger.info(f" Bound user ID `{user.id}` to CustomChat ID `{chat_message.sender_id}`")

    def extract_platform_id(self, user: AbstractUser) -> Optional[str]:
        return user.custom_chat_id

    def create_main_menu_keyboard(self, language: Optional[Language]) -> Any:
        return self.create_menu_keyboard_from(
            localize_list(UserFunctionality.pretty_values_not_localized(), language)
        )

    def create_quick_feedback_menu(self, language: Optional[Language]) -> Any:
        return self.create_quick_menu_from(
            localize_list(Usefulness.pretty_values_not_localized(), language)
        )
