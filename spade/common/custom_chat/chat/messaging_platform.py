import logging
from io import BytesIO
from typing import Optional, List, Mapping, Union

import emoji
from aiogram.types import ParseMode

from common.chat.message.factory import ChatMessageFactory
from common.chat.message.types import ChatMessage
from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform, ChatAction
from common.custom_chat.chat.message_content_factory import CustomChatMessageContentFactory
from common.custom_chat.chat.message_utils import WebSocketMessageUtils
from common.custom_chat.client_notification_manager import ClientNotificationManager
from common.custom_chat.connected_clients_manager import WebSocketConnectedClientsManager
from common.custom_chat.message_dao import AbstractMessageDAO

logger = logging.getLogger(__name__)


class CustomChatMessagingPlatform(AbstractMessagingPlatform):
    """Actual implementation of custom chat messaging platform """

    def __init__(self, _unused_chat_api_token, clients_manager: WebSocketConnectedClientsManager,
                 messages_dao: Optional[AbstractMessageDAO] = None,
                 notification_manager: Optional[ClientNotificationManager] = None):

        # No api token needed in custom chat for now

        self._websocket_clients_manager = clients_manager
        self._notification_manager = notification_manager

        self._message_dao = messages_dao

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

    async def download_image(self, file_id: str) -> BytesIO:
        # TODO: Implement image receiving via websocket
        pass

    async def send_media_group(self, recipient_id: str, media_paths_to_descriptions: Mapping[str, str],
                               reply_to_message_id: str = None) -> List[ChatMessage]:
        # TODO: Implement bulk image sending via websocket
        pass

    async def send_venue(self, recipient_id: str, title: str, address: str, latitude: float, longitude: float,
                         reply_to_message_id: str = None, custom_keyboard_obj=None,
                         quick_reply_menu_obj=None) -> ChatMessage:
        # TODO: Implement an equivalent for venues in Telegram for websocket
        pass

    async def _send_web_socket_message(self, recipient_id: str, message_content: dict) -> bool:
        """
        Utility function encapsulating the logic to send a message to some recipient.
        Returns true on successful send, false otherwise
        """

        prepared_message = WebSocketMessageUtils.preprocess_for_websocket(message_content)
        client_websocket = self._websocket_clients_manager.get_client(recipient_id)
        if client_websocket:
            client_websocket.sendMessage(prepared_message)
            return True
        else:
            logger.warning(f" Cannot send the message over websocket to client ID `{recipient_id}` "
                           f"because the client has no opened connection with the server currently...")
            return False

    async def _after_sending_management(self, recipient_id: str, message_content: dict, successful_send: bool):
        """Refactoring of common things to do after sending a text chat message"""

        if not successful_send and self._notification_manager:  # Save for future notification
            self._notification_manager.add_message(recipient_id, message_content)

        if self._message_dao:
            self._message_dao.insert(message_content)
        self._last_sent_messages.append(ChatMessageFactory.from_raw_strings_dictionary(message_content))
        self._trim_messages_cache()

    async def send_message(self, recipient_id: str, message_text: str, reply_to_message_id: str = None,
                           custom_keyboard_obj=None, quick_reply_menu_obj=None, disable_web_page_preview: bool = False,
                           parse_mode: Union[str, None] = ParseMode.MARKDOWN) -> ChatMessage:
        message_content = CustomChatMessageContentFactory.create_message_content(
            emoji.emojize(message_text),
            reply_to_message_id,
            custom_keyboard_obj,
            quick_reply_menu_obj
        )

        successful_send = await self._send_web_socket_message(recipient_id, message_content)
        await self._after_sending_management(recipient_id, message_content, successful_send)
        return self._last_sent_messages[-1]

    async def send_chat_action(self, recipient_id: str, chat_action_obj: ChatAction):
        message_content = CustomChatMessageContentFactory.create_chat_action_content(chat_action_obj)
        await self._send_web_socket_message(recipient_id, message_content)

    async def send_image(self, recipient_id: str, image_absolute_path: str, image_description: str,
                         reply_to_message_id: str = None,
                         custom_keyboard_obj=None,
                         quick_reply_menu_obj=None) -> ChatMessage:
        return await self.send_animation(
            recipient_id, image_absolute_path, image_description, reply_to_message_id, custom_keyboard_obj,
            quick_reply_menu_obj
        )

    async def send_animation(self, recipient_id: str, animation_path: str, image_description: str,
                             reply_to_message_id: str = None,
                             custom_keyboard_obj=None,
                             quick_reply_menu_obj=None) -> ChatMessage:
        message_content = CustomChatMessageContentFactory.create_image_content(
            animation_path,
            emoji.emojize(image_description),
            reply_to_message_id,
            custom_keyboard_obj,
            quick_reply_menu_obj
        )
        successful_send = await self._send_web_socket_message(recipient_id, message_content)
        await self._after_sending_management(recipient_id, message_content, successful_send)
        return self._last_sent_messages[-1]

    async def edit_message(self, recipient_id: str, to_modify_message_id: str, new_message_text: str,
                           quick_reply_menu_obj=None):
        message_content = CustomChatMessageContentFactory.create_edit_message_content(
            to_modify_message_id, emoji.emojize(new_message_text), quick_reply_menu_obj
        )
        await self._send_web_socket_message(recipient_id, message_content)
        if self._message_dao:
            new_message_content = CustomChatMessageContentFactory.create_message_content(
                emoji.emojize(new_message_text), quick_reply_menu_obj=quick_reply_menu_obj,
                message_id=to_modify_message_id
            )
            self._message_dao.update(to_modify_message_id, new_message_content)

    async def edit_quick_replies_for_message_id(self, recipient_id: str, to_modify_message_id: str,
                                                quick_reply_menu_obj=None):
        message_content = CustomChatMessageContentFactory.create_edit_message_quick_replies_content(
            to_modify_message_id, quick_reply_menu_obj
        )
        await self._send_web_socket_message(recipient_id, message_content)

    async def notify_quick_reply_received(self, reply_to_quick_reply_id: str, notification_text: Optional[str] = None):
        pass  # In the custom chat system this is useless

    async def delete_message(self, recipient_id: str, message_id: str):
        message_content = CustomChatMessageContentFactory.create_delete_message_content(message_id)
        await self._send_web_socket_message(recipient_id, message_content)
        if self._message_dao:
            self._message_dao.delete_by_id(message_id)
