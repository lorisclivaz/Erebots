import logging
from datetime import datetime
from enum import Enum
from typing import Optional

import emoji

from common.chat.language_enum import Language
from common.chat.message.types import ChatActualMessage, ChatQuickReply
from common.chat.platform.types import ChatPlatform

logger = logging.getLogger(__name__)


class CustomChatMessage(ChatActualMessage):
    """A wrapper class for CustomChat messages"""

    @property
    def sender_id(self) -> str:
        """Unique identifier for this chat."""
        return self._strings_dictionary[CustomChatMessage.Fields.SENDER_ID_FIELD.value]

    @property
    def sender_first_name(self) -> Optional[str]:
        return self._strings_dictionary.get(CustomChatMessage.Fields.SENDER_FIRST_NAME_FIELD.value, None)

    @property
    def sender_last_name(self) -> Optional[str]:
        return self._strings_dictionary.get(CustomChatMessage.Fields.SENDER_LAST_NAME_FIELD.value, None)

    @property
    def sender_locale(self) -> Optional[Language]:
        language = self._strings_dictionary.get(CustomChatMessage.Fields.SENDER_LANGUAGE_CODE_FIELD.value, None)
        return Language.from_ietf_tag(language)

    @property
    def message_id(self) -> str:
        return self._strings_dictionary[CustomChatMessage.Fields.MESSAGE_ID_FIELD.value]

    @property
    def message_timestamp(self) -> datetime:
        string_timestamp = self._strings_dictionary[CustomChatMessage.Fields.DATE_FIELD.value]
        return datetime.fromtimestamp(float(string_timestamp))

    @property
    def message_text(self) -> str:
        """The actual UTF-8 text of the message, 0-4096 characters, demojized"""
        return emoji.demojize(self._strings_dictionary[CustomChatMessage.Fields.TEXT_FIELD.value])

    @property
    def photo(self) -> str:
        return self._strings_dictionary[CustomChatMessage.Fields.PHOTO_FIELD.value]

    @property
    def chat_platform(self) -> ChatPlatform:
        return ChatPlatform.CUSTOM_CHAT

    @property
    def is_quick_reply(self) -> bool:
        return CustomChatMessage._is_quick_reply(self._strings_dictionary)

    @staticmethod
    def from_strings_dictionary(strings_dictionary):
        """A factory method for all CustomChatMessages returning correct sub-instance"""
        if CustomChatMessage._is_quick_reply(strings_dictionary):
            return CustomChatQuickReply(strings_dictionary)
        else:
            return CustomChatMessage(strings_dictionary)

    @staticmethod
    def _is_quick_reply(strings_dictionary) -> bool:
        """A method containing the logic to determine if a strings_dictionary is from a quick reply or not"""
        is_quick_reply = strings_dictionary.get(CustomChatMessage.Fields.IS_QUICK_REPLY_FIELD.value, None)
        if is_quick_reply is None:
            return False
        elif is_quick_reply == "true" or is_quick_reply == "True" or is_quick_reply is True:
            return True
        else:
            return False

    def to_json(self) -> dict:
        return {
            CustomChatMessage.Fields.MESSAGE_ID_FIELD.value:
                self._strings_dictionary[CustomChatMessage.Fields.MESSAGE_ID_FIELD.value],
            CustomChatMessage.Fields.SENDER_ID_FIELD.value:
                self._strings_dictionary[CustomChatMessage.Fields.SENDER_ID_FIELD.value],
            CustomChatMessage.Fields.SENDER_FIRST_NAME_FIELD.value:
                self._strings_dictionary.get(CustomChatMessage.Fields.SENDER_FIRST_NAME_FIELD.value, None),
            CustomChatMessage.Fields.SENDER_LAST_NAME_FIELD.value:
                self._strings_dictionary.get(CustomChatMessage.Fields.SENDER_LAST_NAME_FIELD.value, None),
            CustomChatMessage.Fields.SENDER_LANGUAGE_CODE_FIELD.value:
                self._strings_dictionary.get(CustomChatMessage.Fields.SENDER_LANGUAGE_CODE_FIELD.value, None),
            CustomChatMessage.Fields.DATE_FIELD.value:
                self._strings_dictionary[CustomChatMessage.Fields.DATE_FIELD.value],
            CustomChatMessage.Fields.TEXT_FIELD.value:
                self._strings_dictionary[CustomChatMessage.Fields.TEXT_FIELD.value],
            CustomChatMessage.Fields.PHOTO_FIELD.value:
                self._strings_dictionary.get(CustomChatMessage.Fields.PHOTO_FIELD.value, None),
        }

    class Fields(Enum):
        """A class containing all CustomChat messages field names"""

        MESSAGE_ID_FIELD = "message_id"
        """Unique message identifier inside this chat"""

        REPLY_TO_MESSAGE_ID_FIELD = "reply_to_message_id"
        """The field holding the message id to which this replies"""

        SENDER_ID_FIELD = "sender_id"
        """Unique identifier for this chat. """

        SENDER_FIRST_NAME_FIELD = "sender_first_name"
        """*Optional.* First name of the other party in a private chat"""

        SENDER_LAST_NAME_FIELD = "sender_last_name"
        """*Optional.* Last name of the other party in a private chat"""

        SENDER_LANGUAGE_CODE_FIELD = "sender_language_code"
        """*Optional.* `IETF language tag <https://en.wikipedia.org/wiki/IETF_language_tag>`_ of the user's language"""

        DATE_FIELD = "date"
        """Date the message was sent in Unix time"""

        TEXT_FIELD = "text"
        """*Optional.* For text messages, the actual UTF-8 text of the message, 0-4096 characters"""

        PHOTO_FIELD = "photo"
        """*Optional.* For pictures, the base64 encoded string of the photo"""

        IS_QUICK_REPLY_FIELD = "is_quick_reply"
        """Field signaling if this message is a quick reply or not, if not present is considered false"""


class CustomChatQuickReply(CustomChatMessage, ChatQuickReply):
    """A class representing CustomChat callbacks (which are quick replies)"""

    @property
    def quick_reply_about_msg_id(self) -> str:
        return self._strings_dictionary[CustomChatMessage.Fields.REPLY_TO_MESSAGE_ID_FIELD.value]

    @property
    def quick_reply_payload(self) -> str:
        return self.message_text
