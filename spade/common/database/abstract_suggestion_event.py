from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from common.database.json_convertible import AbstractJsonConvertible


class AbstractSuggestionEvent(AbstractJsonConvertible, ABC):
    """Abstract base class for all events which carry a suggestion which could be evaluated by the user"""

    @property
    @abstractmethod
    def datetime(self) -> datetime:
        """The suggestion event datetime field"""
        pass

    @datetime.setter
    @abstractmethod
    def datetime(self, new_value: datetime):
        """Setter for datetime field"""
        pass

    @property
    @abstractmethod
    def suggestion_message_id(self) -> Optional[str]:
        """The suggestion event suggestion_message_id field"""
        pass

    @suggestion_message_id.setter
    @abstractmethod
    def suggestion_message_id(self, new_value: str):
        """Setter for suggestion_message_id field"""
        pass

    @property
    @abstractmethod
    def suggestion_usefulness(self) -> Optional[str]:
        """The suggestion event suggestion_usefulness field"""
        pass

    @suggestion_usefulness.setter
    @abstractmethod
    def suggestion_usefulness(self, new_value: str):
        """Setter for suggestion_usefulness field"""
        pass
