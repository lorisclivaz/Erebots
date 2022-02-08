from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Mapping

from common.chat.language_enum import Language
from common.chat.platform.types import ChatPlatform
from common.utils.dictionaries import flatten_dictionary


class ChatMessage(ABC):
    """A base class for all chat messages, handled by the system"""

    def __init__(self, message_dictionary):
        self._strings_dictionary = flatten_dictionary(message_dictionary)

    @property
    @abstractmethod
    def sender_id(self) -> str:
        """Unique ID identifying the user sending this message"""
        pass

    @property
    @abstractmethod
    def sender_first_name(self) -> Optional[str]:
        """The user first name"""
        pass

    @property
    @abstractmethod
    def sender_last_name(self) -> Optional[str]:
        """The user last name"""
        pass

    @property
    @abstractmethod
    def sender_locale(self) -> Optional[Language]:
        """Optionally the user locale"""
        pass

    @property
    @abstractmethod
    def message_id(self) -> str:
        """The unique ID of this message"""
        pass

    @property
    @abstractmethod
    def message_timestamp(self) -> datetime:
        """The timestamp of when the message was sent"""
        pass

    @property
    @abstractmethod
    def message_text(self) -> str:
        """The message text content (with no emoji -- demojized)"""
        pass

    @property
    @abstractmethod
    def chat_platform(self) -> ChatPlatform:
        """The chat platform from which this message comes from"""
        pass

    @property
    def is_quick_reply(self) -> bool:
        """Whether this message is a quick reply to our sent message, or not"""
        return isinstance(self, ChatQuickReply)

    @property
    def strings_dictionary(self) -> Mapping[str, Optional[str]]:
        """Returns a copy of the raw strings dictionary held"""
        return self._strings_dictionary.copy()

    def __str__(self):
        return str(self._strings_dictionary)


class ChatActualMessage(ChatMessage, ABC):
    """A class representing messages sent by the user, as text to the chat"""

    def __init__(self, message_dictionary):
        super().__init__(message_dictionary)

    @abstractmethod
    def to_json(self) -> dict:
        pass


class ChatQuickReply(ChatMessage, ABC):
    """A class representing those messages which are predefined quick replies, made available into the chat"""

    def __init__(self, message_dictionary):
        super().__init__(message_dictionary)

    @property
    @abstractmethod
    def quick_reply_about_msg_id(self) -> str:
        """The ID of the message to which this quick reply refers to"""
        pass

    @property
    @abstractmethod
    def quick_reply_payload(self) -> str:
        """The payload of the quick reply"""
        pass
