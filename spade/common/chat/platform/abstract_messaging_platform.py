import asyncio
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Optional, List, Mapping, Union

from aiogram.types import ParseMode

from common.chat.message.types import ChatMessage
from common.utils.enums import ValuesMixin


class ChatAction(ValuesMixin):
    """An enumeration for chat actions that can be sent to the user through a messaging platform"""

    TYPING = "typing"
    """Show that the bot is typing"""

    UPLOAD_PHOTO = "upload_photo"
    """Show that the bot is uploading images"""


class AbstractMessagingPlatform(ABC):
    """An abstract class modelling in abstract a messaging platform"""

    SENT_MESSAGES_CACHE_MAX_SIZE = 15
    """The max amount of messages stored in "sent_messages" """

    @property
    @abstractmethod
    def last_sent_message(self) -> Optional[ChatMessage]:
        """A property holding always the last sent message reference, if any"""
        pass

    @property
    @abstractmethod
    def sent_messages(self) -> List[ChatMessage]:
        """A property holding the list of messages sent by this messaging platform, if any"""
        pass

    @abstractmethod
    async def send_message(self, recipient_id: str, message_text: str, reply_to_message_id: str = None,
                           custom_keyboard_obj=None, quick_reply_menu_obj=None, disable_web_page_preview: bool = False,
                           parse_mode: Union[str, None] = ParseMode.MARKDOWN) -> ChatMessage:
        """
        A method to send a message through a messaging platform

        "custom_keyboard_obj" and "quick_reply_menu_obj" are intended to be mutually exclusive,
        if both are present "custom_keyboard_obj" should be taken

        :returns: The sent message
        """
        pass

    @abstractmethod
    async def send_chat_action(self, recipient_id: str, chat_action_obj: ChatAction):
        """A method to send a chat action to user (like "typing", etc...)"""
        pass

    @abstractmethod
    async def send_image(self, recipient_id: str, image_absolute_path: str, image_description: str,
                         reply_to_message_id: str = None,
                         custom_keyboard_obj=None,
                         quick_reply_menu_obj=None) -> ChatMessage:
        """
        A method to send an image through the messaging platform

        "custom_keyboard_obj" and "quick_reply_menu_obj" are intended to be mutually exclusive,
        if both are present "custom_keyboard_obj" should be taken

        :returns: The sent message
        """
        pass

    @abstractmethod
    async def download_image(self, file_id: str) -> BytesIO:
        """
        A method to download a received image through the messaging platform
        """
        pass

    @abstractmethod
    async def send_animation(self, recipient_id: str, animation_path: str, image_description: str,
                             reply_to_message_id: str = None,
                             custom_keyboard_obj=None,
                             quick_reply_menu_obj=None) -> ChatMessage:
        """
        A method to send an animation (like GIF) stored locally or from a link, through the messaging platform

        "custom_keyboard_obj" and "quick_reply_menu_obj" are intended to be mutually exclusive,
        if both are present "custom_keyboard_obj" should be taken

        :returns: The sent message
        """
        pass

    @abstractmethod
    async def send_media_group(self, recipient_id: str, media_paths_to_descriptions: Mapping[str, str],
                               reply_to_message_id: str = None) -> List[ChatMessage]:
        """
        A method to send a group of media

        :returns: The list of sent messages
        """

    @abstractmethod
    async def send_venue(self, recipient_id: str, title: str, address: str, latitude: float, longitude: float,
                         reply_to_message_id: str = None,
                         custom_keyboard_obj=None,
                         quick_reply_menu_obj=None) -> ChatMessage:
        """
        A method to send a venue through the messaging platform

        "custom_keyboard_obj" and "quick_reply_menu_obj" are intended to be mutually exclusive,
        if both are present "custom_keyboard_obj" should be taken

        :returns: The sent message
        """
        pass

    @abstractmethod
    async def edit_message(self, recipient_id: str, to_modify_message_id: str, new_message_text: str,
                           quick_reply_menu_obj=None):
        """
        A method to modify a previously sent message, and optionally the quick replies attached to it

        If "quick_reply_menu_obj" is left None, then the quick replies are erased from the chat
        """
        pass

    @abstractmethod
    async def edit_quick_replies_for_message_id(self, recipient_id: str, to_modify_message_id: str,
                                                quick_reply_menu_obj=None):
        """
        A method to modify the quick replies available to user for a message

        If "quick_reply_menu_obj" is left None, then the quick replies are erased from the chat
        """
        pass

    @abstractmethod
    async def notify_quick_reply_received(self, reply_to_quick_reply_id: str, notification_text: Optional[str] = None):
        """
        A method to notify the user that its quick reply was received, with temporary non-invasive notification

        If "notification_text" is left None, the user will not see anything but the client will know
        that the command has been handled
        """
        pass

    @abstractmethod
    async def delete_message(self, recipient_id: str, message_id: str):
        """
        A method to delete a chat message
        """
        pass

    async def send_message_after_sleep(
            self, recipient_id: str, message_text: str, reply_to_message_id: str = None, custom_keyboard_obj=None,
            quick_reply_menu_obj=None, sleep_seconds: float = 1, disable_web_page_preview: bool = False,
            parse_mode: Union[str, None] = ParseMode.MARKDOWN
    ) -> ChatMessage:
        """
        A method to send a message through a messaging platform, after observing some sleep time

        :returns: The sent message
        """
        await self.send_chat_action(recipient_id, ChatAction.TYPING)
        await asyncio.sleep(sleep_seconds)
        return await self.send_message(
            recipient_id, message_text, reply_to_message_id, custom_keyboard_obj, quick_reply_menu_obj,
            disable_web_page_preview=disable_web_page_preview,
            parse_mode=parse_mode
        )
