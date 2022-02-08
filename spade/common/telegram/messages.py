import logging
from datetime import datetime
from enum import Enum
from typing import Optional

from aiogram.utils import emoji

from common.chat.language_enum import Language
from common.chat.message.types import ChatActualMessage, ChatQuickReply
from common.chat.platform.types import ChatPlatform

logger = logging.getLogger(__name__)


class TelegramMessage(ChatActualMessage):
    """A wrapper class for Telegram messages"""

    @property
    def sender_id(self) -> str:
        """Unique identifier for this chat. This number may be greater than 32 bits and some programming languages
        may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit
        integer or double-precision float type are safe for storing this identifier. """
        return self._strings_dictionary[TelegramMessage.Fields.CHAT_ID_FIELD.value]

    @property
    def sender_first_name(self) -> Optional[str]:
        return self._strings_dictionary.get(TelegramMessage.Fields.CHAT_FIRST_NAME_FIELD.value, None)

    @property
    def sender_last_name(self) -> Optional[str]:
        return self._strings_dictionary.get(TelegramMessage.Fields.CHAT_LAST_NAME_FIELD.value, None)

    @property
    def sender_locale(self) -> Optional[Language]:
        language = self._strings_dictionary.get(TelegramMessage.Fields.FROM_LANGUAGE_CODE_FIELD.value, None)
        return Language.from_ietf_tag(language)

    @property
    def message_id(self):
        return self._strings_dictionary[TelegramMessage.Fields.MESSAGE_ID_FIELD.value]

    @property
    def message_timestamp(self) -> datetime:
        string_timestamp = self._strings_dictionary[TelegramMessage.Fields.DATE_FIELD.value]
        return datetime.fromtimestamp(float(string_timestamp))

    @property
    def message_text(self) -> str:
        """The actual UTF-8 text of the message, 0-4096 characters, demojized"""
        return emoji.demojize(self._strings_dictionary[TelegramMessage.Fields.TEXT_FIELD.value])

    @property
    def chat_platform(self) -> ChatPlatform:
        return ChatPlatform.TELEGRAM

    @property
    def is_quick_reply(self) -> bool:
        return TelegramMessage._is_quick_reply(self._strings_dictionary)

    @staticmethod
    def from_strings_dictionary(strings_dictionary):
        """A factory method for all TelegramMessages returning correct sub-instance"""
        if TelegramMessage._is_quick_reply(strings_dictionary):
            return TelegramCallback(strings_dictionary)
        else:
            return TelegramMessage(strings_dictionary)

    @staticmethod
    def _is_quick_reply(strings_dictionary):
        """A method containing the logic to determine if a strings_dictionary is from a quick reply or not"""
        return strings_dictionary.get(TelegramCallback.Fields.DATA_FIELD.value, None) is not None

    def to_json(self) -> dict:
        return {
            TelegramMessage.Fields.CHAT_ID_FIELD.value:
                self._strings_dictionary[TelegramMessage.Fields.CHAT_ID_FIELD.value],
            TelegramMessage.Fields.CHAT_FIRST_NAME_FIELD.value:
                self._strings_dictionary[TelegramMessage.Fields.CHAT_FIRST_NAME_FIELD.value],
            TelegramMessage.Fields.CHAT_LAST_NAME_FIELD.value:
                self._strings_dictionary[TelegramMessage.Fields.CHAT_LAST_NAME_FIELD.value],
            TelegramMessage.Fields.FROM_LANGUAGE_CODE_FIELD.value:
                self._strings_dictionary[TelegramMessage.Fields.FROM_LANGUAGE_CODE_FIELD.value],
            TelegramMessage.Fields.MESSAGE_ID_FIELD.value:
                self._strings_dictionary[TelegramMessage.Fields.MESSAGE_ID_FIELD.value],
            TelegramMessage.Fields.DATE_FIELD.value:
                self._strings_dictionary[TelegramMessage.Fields.DATE_FIELD.value],
            TelegramMessage.Fields.TEXT_FIELD.value:
                self._strings_dictionary[TelegramMessage.Fields.TEXT_FIELD.value],
        }

    class Fields(Enum):
        """A class containing all Telegram messages field names"""

        CHAT_ID_FIELD = "chat_id"
        """Unique identifier for this chat. This number may be greater than 32 bits and some programming languages may 
        have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or 
        double-precision float type are safe for storing this identifier. """

        CHAT_FIRST_NAME_FIELD = "chat_first_name"
        """*Optional.* First name of the other party in a private chat"""

        CHAT_LAST_NAME_FIELD = "chat_last_name"
        """*Optional.* Last name of the other party in a private chat"""

        FROM_LANGUAGE_CODE_FIELD = "from_language_code"
        """*Optional.* `IETF language tag <https://en.wikipedia.org/wiki/IETF_language_tag>`_ of the user's language"""

        MESSAGE_ID_FIELD = "message_id"
        """Unique message identifier inside this chat"""

        DATE_FIELD = "date"
        """Date the message was sent in Unix time"""

        TEXT_FIELD = "text"
        """*Optional.* For text messages, the actual UTF-8 text of the message, 0-4096 characters"""


class TelegramCallback(TelegramMessage, ChatQuickReply):
    """A class representing Telegram callbacks (which are quick replies)"""

    @property
    def sender_id(self) -> str:
        return self._strings_dictionary[TelegramCallback.Fields.FROM_ID_FIELD.value]

    @property
    def sender_first_name(self) -> Optional[str]:
        return self._strings_dictionary.get(TelegramCallback.Fields.FROM_FIRST_NAME_FIELD.value, None)

    @property
    def sender_last_name(self) -> Optional[str]:
        return self._strings_dictionary.get(TelegramCallback.Fields.FROM_LAST_NAME_FIELD.value, None)

    @property
    def message_id(self):
        return self._strings_dictionary[TelegramCallback.Fields.ID_FIELD.value]

    @property
    def message_timestamp(self) -> datetime:
        string_timestamp = self._strings_dictionary[TelegramCallback.Fields.MESSAGE_DATE_FIELD.value]
        return datetime.fromtimestamp(float(string_timestamp))

    @property
    def message_text(self) -> str:
        return self.quick_reply_payload

    @property
    def quick_reply_about_msg_id(self) -> str:
        return self._strings_dictionary[TelegramCallback.Fields.MESSAGE_MESSAGE_ID_FIELD.value]

    @property
    def quick_reply_payload(self) -> str:
        return self._strings_dictionary[TelegramCallback.Fields.DATA_FIELD.value]

    class Fields(Enum):
        """A class containing all Telegram callback field names"""

        FROM_ID_FIELD = "from_id"
        """Unique identifier for this chat. This number may be greater than 32 bits and some programming languages may 
        have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or 
        double-precision float type are safe for storing this identifier. """

        FROM_FIRST_NAME_FIELD = "from_first_name"
        """*Optional.* First name of the other party in a private chat"""

        FROM_LAST_NAME_FIELD = "from_last_name"
        """*Optional.* Last name of the other party in a private chat"""

        ID_FIELD = "id"
        """Unique message identifier inside this chat"""

        MESSAGE_DATE_FIELD = "message_date"
        """Date the message was sent in Unix time"""

        MESSAGE_MESSAGE_ID_FIELD = "message_message_id"
        """The field holding the message to which this quick reply was made"""

        DATA_FIELD = "data"
        """The field is intended to hold callback data for callback messages"""
