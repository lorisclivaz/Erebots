import logging
import math
from abc import ABC
from typing import Any, Collection, Dict

import validators
from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.utils import emoji

from common.agent.strategies.abstract_handling_strategies import AbstractHandlingStrategies

logger = logging.getLogger(__name__)


class TelegramMessageHandlingStrategiesMixin(AbstractHandlingStrategies, ABC):
    """Mixin to help implement concrete strategies for Telegram messaging platform"""

    def create_menu_keyboard_from(self, option_list: Collection[str], row_width: int = None) -> Any:
        if len(option_list) > 0:
            if row_width is None:
                row_width = int(math.sqrt(len(option_list)))
            keyboard = ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=row_width
            )
            keyboard.add(*[KeyboardButton(emoji.emojize(option)) for option in option_list])
        else:
            keyboard = self.create_show_normal_keyboard()

        return keyboard

    def create_quick_menu_from(self, option_list: Collection[str]) -> Any:
        keyboard = InlineKeyboardMarkup(row_width=4)
        keyboard.add(*[InlineKeyboardButton(emoji.emojize(option), callback_data=option) for option in option_list])
        return keyboard

    def create_inline_menu_from(self, option_dict: Dict[str, str], row_width: int = 3) -> Any:
        keyboard = InlineKeyboardMarkup(row_width=row_width)
        for button_text, payload in option_dict.items():
            if validators.url(payload):
                keyboard.add(*[InlineKeyboardButton(emoji.emojize(button_text), url=payload)])
            else:
                keyboard.add(*[InlineKeyboardButton(emoji.emojize(button_text), callback_data=payload)])
        return keyboard

    def create_show_normal_keyboard(self):
        return ReplyKeyboardRemove()
