import logging
from typing import Optional, List, Mapping, Union

from aiogram import Bot, types
from aiogram.types import ParseMode, InputMediaPhoto
from aiogram.utils import emoji

from common.chat.message.types import ChatMessage
from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform, ChatAction
from common.telegram.agent.integration import preprocess_and_label_telegram_message

logger = logging.getLogger(__name__)


class TelegramMessagingPlatform(AbstractMessagingPlatform):
    """Actual implementation of telegram messaging platform """

    def __init__(self, telegram_api_token):
        self.telegram_bot = Bot(telegram_api_token)

        self._last_sent_messages: List[ChatMessage] = []

    def _trim_messages_cache(self):
        """Utility method to implement messages cache trimming"""
        # It takes always only the last "MAX_SIZE" elements
        self._last_sent_messages = self._last_sent_messages[-self.SENT_MESSAGES_CACHE_MAX_SIZE:]

    @property
    def last_sent_message(self) -> Optional[ChatMessage]:
        return self._last_sent_messages[-1] if self._last_sent_messages else None

    @property
    def sent_messages(self) -> List[ChatMessage]:
        return self._last_sent_messages.copy()

    async def send_message(self, recipient_id: str, message_text: str, reply_to_message_id: str = None,
                           custom_keyboard_obj=None, quick_reply_menu_obj=None,
                           disable_web_page_preview: bool = False,
                           parse_mode: Union[str, None] = ParseMode.MARKDOWN) -> ChatMessage:
        sent_message = await self.telegram_bot.send_message(
            recipient_id,
            emoji.emojize(message_text),
            parse_mode,
            reply_to_message_id=_int_or_none(reply_to_message_id),
            reply_markup=custom_keyboard_obj if custom_keyboard_obj else quick_reply_menu_obj,
            disable_web_page_preview=disable_web_page_preview
        )
        self._last_sent_messages.append(preprocess_and_label_telegram_message(sent_message))
        self._trim_messages_cache()
        return self._last_sent_messages[-1]

    async def send_chat_action(self, recipient_id: str, chat_action_obj: ChatAction):
        if ChatAction.TYPING == chat_action_obj:
            return await self.telegram_bot.send_chat_action(recipient_id, "typing")
        elif ChatAction.UPLOAD_PHOTO == chat_action_obj:
            return await self.telegram_bot.send_chat_action(recipient_id, "upload_photo")
        else:
            logger.info(f" No chat action implemented for Telegram related to {chat_action_obj}")

    async def send_image(self, recipient_id: str, image_absolute_path: str, image_description: str,
                         reply_to_message_id: str = None,
                         custom_keyboard_obj=None,
                         quick_reply_menu_obj=None) -> ChatMessage:
        image_file = types.InputFile(image_absolute_path)

        sent_message = await self.telegram_bot.send_photo(
            recipient_id,
            image_file,
            caption=emoji.emojize(image_description),
            reply_to_message_id=_int_or_none(reply_to_message_id),
            reply_markup=custom_keyboard_obj if custom_keyboard_obj else quick_reply_menu_obj
        )
        self._last_sent_messages.append(preprocess_and_label_telegram_message(sent_message))
        self._trim_messages_cache()
        return self._last_sent_messages[-1]

    async def download_image(self, file_id: str):
        return await self.telegram_bot.download_file_by_id(
            file_id=file_id
        )

    async def send_animation(self, recipient_id: str, animation_path: str, image_description: str,
                             reply_to_message_id: str = None,
                             custom_keyboard_obj=None,
                             quick_reply_menu_obj=None) -> ChatMessage:

        if animation_path.startswith("http"):
            animation_to_be_sent = animation_path
        else:
            animation_to_be_sent = types.InputFile(animation_path)

        sent_message = await self.telegram_bot.send_animation(
            recipient_id,
            animation_to_be_sent,
            caption=emoji.emojize(image_description),
            reply_to_message_id=_int_or_none(reply_to_message_id),
            reply_markup=custom_keyboard_obj if custom_keyboard_obj else quick_reply_menu_obj
        )
        self._last_sent_messages.append(preprocess_and_label_telegram_message(sent_message))
        self._trim_messages_cache()
        return self._last_sent_messages[-1]

    async def send_media_group(self, recipient_id: str, media_paths_to_descriptions: Mapping[str, str],
                               reply_to_message_id: str = None) -> List[ChatMessage]:
        media_array = [
            InputMediaPhoto(
                path if path.startswith("http") else types.InputFile(path),
                caption=emoji.emojize(description)
            )
            for path, description in media_paths_to_descriptions.items()
        ]

        sent_messages = await self.telegram_bot.send_media_group(
            recipient_id,
            media_array,
            reply_to_message_id=_int_or_none(reply_to_message_id)
        )
        preprocessed_sent_messages = [preprocess_and_label_telegram_message(message) for message in sent_messages]
        self._last_sent_messages.extend(preprocessed_sent_messages)
        self._trim_messages_cache()
        return preprocessed_sent_messages

    async def send_venue(self, recipient_id: str, title: str, address: str, latitude: float, longitude: float,
                         reply_to_message_id: str = None,
                         custom_keyboard_obj=None,
                         quick_reply_menu_obj=None) -> ChatMessage:

        sent_message = await self.telegram_bot.send_venue(
            chat_id=recipient_id,
            title=title,
            address=address,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=_int_or_none(reply_to_message_id),
            reply_markup=custom_keyboard_obj if custom_keyboard_obj else quick_reply_menu_obj
        )
        self._last_sent_messages.append(preprocess_and_label_telegram_message(sent_message))
        self._trim_messages_cache()
        return self._last_sent_messages[-1]

    async def edit_message(self, recipient_id: str, to_modify_message_id: str, new_message_text: str,
                           quick_reply_menu_obj=None):
        return await self.telegram_bot.edit_message_text(
            emoji.emojize(new_message_text),
            recipient_id,
            _int_or_none(to_modify_message_id),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=quick_reply_menu_obj
        )

    async def edit_quick_replies_for_message_id(self, recipient_id: str, to_modify_message_id: str,
                                                quick_reply_menu_obj=None):
        return await self.telegram_bot.edit_message_reply_markup(
            recipient_id,
            message_id=_int_or_none(to_modify_message_id),
            reply_markup=quick_reply_menu_obj
        )

    async def notify_quick_reply_received(self, reply_to_quick_reply_id: str, notification_text: Optional[str] = None):
        return await self.telegram_bot.answer_callback_query(
            reply_to_quick_reply_id,
            emoji.emojize(notification_text) if notification_text else None
        )

    async def delete_message(self, recipient_id: str, message_id: str):
        return await self.telegram_bot.delete_message(recipient_id, _int_or_none(message_id))


def _int_or_none(some_str: Optional[str]) -> Optional[int]:
    """Utility function to convert something to int if it's not None"""

    return int(some_str) if some_str else None
