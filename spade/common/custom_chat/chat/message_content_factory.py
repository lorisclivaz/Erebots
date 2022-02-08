import uuid
from datetime import datetime
from enum import Enum

from common.chat.platform.abstract_messaging_platform import ChatAction
from common.chat.platform.types import ChatPlatform
from common.custom_chat.messages import CustomChatMessage


class CustomChatMessageContentFactory:
    """A factory class to create message contents for CustomChat"""

    MESSAGE_TYPE_JSON_FIELD = "message_type"
    CUSTOM_KEYBOARD_JSON_FIELD = "custom_keyboard"
    QUICK_REPLY_MENU_JSON_FIELD = "quick_reply_menu"
    IMAGE_JSON_FIELD = "image_path"

    class MessageTypes(Enum):
        MESSAGE = "message"
        CHAT_ACTION = "chat_action"
        MODIFY_MESSAGE = "modify_message"
        MODIFY_MESSAGE_QUICK_REPLIES = "modify_quick_replies"
        DELETE_MESSAGE = "delete_message"
        ERROR_MESSAGE = "error"
        IMAGE_MESSAGE = "image"

    @staticmethod
    def create_message_content(message_text: str, reply_to_message_id: str = None,
                               custom_keyboard_obj=None, quick_reply_menu_obj=None, message_id: str = None) -> dict:
        """Returns the raw dictionary representing the message content"""
        return {
            CustomChatMessageContentFactory.MESSAGE_TYPE_JSON_FIELD:
                CustomChatMessageContentFactory.MessageTypes.MESSAGE.value,
            CustomChatMessage.Fields.MESSAGE_ID_FIELD.value: str(uuid.uuid4()) if message_id is None else message_id,
            CustomChatMessage.Fields.DATE_FIELD.value: str(datetime.timestamp(datetime.now())),
            CustomChatMessage.Fields.TEXT_FIELD.value: message_text,
            CustomChatMessage.Fields.REPLY_TO_MESSAGE_ID_FIELD.value: reply_to_message_id,
            CustomChatMessageContentFactory.CUSTOM_KEYBOARD_JSON_FIELD: custom_keyboard_obj,
            CustomChatMessageContentFactory.QUICK_REPLY_MENU_JSON_FIELD: quick_reply_menu_obj,
            ChatPlatform.field_name(): ChatPlatform.CUSTOM_CHAT.value
        }

    @staticmethod
    def create_chat_action_content(chat_action: ChatAction) -> dict:
        """Returns the raw dictionary representing the chat action content"""
        return {
            CustomChatMessageContentFactory.MESSAGE_TYPE_JSON_FIELD:
                CustomChatMessageContentFactory.MessageTypes.CHAT_ACTION.value,
            CustomChatMessage.Fields.MESSAGE_ID_FIELD.value: str(uuid.uuid4()),
            CustomChatMessage.Fields.DATE_FIELD.value: str(datetime.timestamp(datetime.now())),
            CustomChatMessage.Fields.TEXT_FIELD.value: chat_action.value
        }

    @staticmethod
    def create_edit_message_content(to_modify_message_id: str, new_message_text: str,
                                    quick_reply_menu_obj=None) -> dict:
        """Returns the raw dictionary representing the message modification to be sent"""
        return {
            CustomChatMessageContentFactory.MESSAGE_TYPE_JSON_FIELD:
                CustomChatMessageContentFactory.MessageTypes.MODIFY_MESSAGE.value,
            CustomChatMessage.Fields.MESSAGE_ID_FIELD.value: to_modify_message_id,
            CustomChatMessage.Fields.DATE_FIELD.value: str(datetime.timestamp(datetime.now())),
            CustomChatMessage.Fields.TEXT_FIELD.value: new_message_text,
            CustomChatMessageContentFactory.QUICK_REPLY_MENU_JSON_FIELD: quick_reply_menu_obj
        }

    @staticmethod
    def create_edit_message_quick_replies_content(to_modify_message_id: str, quick_reply_menu_obj=None) -> dict:
        """Returns the raw dictionary representing the message modification to be sent"""
        return {
            CustomChatMessageContentFactory.MESSAGE_TYPE_JSON_FIELD:
                CustomChatMessageContentFactory.MessageTypes.MODIFY_MESSAGE_QUICK_REPLIES.value,
            CustomChatMessage.Fields.MESSAGE_ID_FIELD.value: to_modify_message_id,
            CustomChatMessage.Fields.DATE_FIELD.value: str(datetime.timestamp(datetime.now())),
            CustomChatMessageContentFactory.QUICK_REPLY_MENU_JSON_FIELD: quick_reply_menu_obj
        }

    @staticmethod
    def create_delete_message_content(to_delete_message_id: str) -> dict:
        """Returns the raw dictionary representing the message deletion to be sent"""
        return {
            CustomChatMessageContentFactory.MESSAGE_TYPE_JSON_FIELD:
                CustomChatMessageContentFactory.MessageTypes.DELETE_MESSAGE.value,
            CustomChatMessage.Fields.MESSAGE_ID_FIELD.value: to_delete_message_id
        }

    @staticmethod
    def create_error_message_content(message_text: str) -> dict:
        """Returns the raw dictionary representing the error message to be sent"""
        return {
            CustomChatMessageContentFactory.MESSAGE_TYPE_JSON_FIELD:
                CustomChatMessageContentFactory.MessageTypes.ERROR_MESSAGE.value,
            CustomChatMessage.Fields.MESSAGE_ID_FIELD.value: str(uuid.uuid4()),
            CustomChatMessage.Fields.DATE_FIELD.value: str(datetime.timestamp(datetime.now())),
            CustomChatMessage.Fields.TEXT_FIELD.value: message_text
        }

    @staticmethod
    def create_image_content(animation_path: str, image_description: str, reply_to_message_id: str = None,
                             custom_keyboard_obj=None, quick_reply_menu_obj=None) -> dict:
        if animation_path.startswith("http"):
            temp_message = CustomChatMessageContentFactory.create_message_content(
                image_description, reply_to_message_id, custom_keyboard_obj, quick_reply_menu_obj
            )
            temp_message[CustomChatMessageContentFactory.MESSAGE_TYPE_JSON_FIELD] = (
                CustomChatMessageContentFactory.MessageTypes.IMAGE_MESSAGE.value
            )
            temp_message[CustomChatMessageContentFactory.IMAGE_JSON_FIELD] = animation_path
            return temp_message
        else:
            raise Exception(
                f"Provided animation path `${animation_path}` is not a web link. "
                f"Only links are supported in custom chat system"
            )
