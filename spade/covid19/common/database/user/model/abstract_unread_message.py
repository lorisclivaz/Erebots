from abc import ABC, abstractmethod

from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible


class AbstractUnreadMessage(AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing an unread message for a user"""

    @property
    @abstractmethod
    def recipient_id(self) -> str:
        """The recipient of the unread message"""
        pass

    @recipient_id.setter
    @abstractmethod
    def recipient_id(self, new_value: str):
        """Setter for recipient_id field"""
        pass

    @property
    @abstractmethod
    def message_json(self) -> dict:
        """The message_json payload"""
        pass

    @message_json.setter
    @abstractmethod
    def message_json(self, new_value: dict):
        """Setter for message_json field"""
        pass
