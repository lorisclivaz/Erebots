from abc import ABC, abstractmethod

from common.database.json_convertible import AbstractJsonConvertible


class AbstractChatMessage(AbstractJsonConvertible, ABC):
    """An abstract model representing a user ChatMessage"""

    @property
    @abstractmethod
    def user_id(self) -> str:
        """The ChatMessage referred user"""
        pass

    @property
    @abstractmethod
    def message_id(self) -> str:
        """The chat message message_id field"""
        pass

    @message_id.setter
    @abstractmethod
    def message_id(self, new_value: str):
        """Setter for message_id field"""
        pass

    @property
    @abstractmethod
    def payload(self) -> dict:
        """The chat message payload field"""
        pass

    @payload.setter
    @abstractmethod
    def payload(self, new_value: dict):
        """Setter for payload field"""
        pass

    def __str__(self):
        try:
            return f"user_id: {self.user_id}, {self.to_json_string()}"
        except TypeError:
            return self.to_json_string()
