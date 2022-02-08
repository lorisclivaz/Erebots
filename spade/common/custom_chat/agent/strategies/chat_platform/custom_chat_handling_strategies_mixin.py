import logging
import math
from abc import ABC
from typing import Any, Collection

import emoji

from common.agent.strategies.abstract_handling_strategies import AbstractHandlingStrategies
from common.custom_chat.agent.strategies.chat_platform.keybobard_obj_factories import KeyboardObjectFactory

logger = logging.getLogger(__name__)


class CustomChatMessageHandlingStrategiesMixin(AbstractHandlingStrategies, ABC):
    """Mixin to help implement concrete strategies for CustomChat messaging platform"""

    def create_menu_keyboard_from(self, option_list: Collection[str], row_width: int = None) -> Any:
        if len(option_list) > 0:
            computed_row_width = int(math.sqrt(len(option_list)))
            keyboard = KeyboardObjectFactory.create_menu_object(
                [emoji.emojize(option) for option in option_list],
                computed_row_width
            )
        else:
            keyboard = self.create_show_normal_keyboard()

        return keyboard

    def create_quick_menu_from(self, option_list: Collection[str]) -> Any:
        return KeyboardObjectFactory.create_quick_replies_object([emoji.emojize(option) for option in option_list])

    def create_show_normal_keyboard(self):
        return KeyboardObjectFactory.create_show_normal_keyboard_object()
