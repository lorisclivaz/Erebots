from abc import ABC, abstractmethod
from datetime import datetime

from common.database.json_convertible import AbstractJsonConvertible


class AbstractCacheData(AbstractJsonConvertible, ABC):
    """An abstract model representing cache data"""

    @property
    @abstractmethod
    def id(self) -> str:
        """The user id"""
        pass

    @property
    @abstractmethod
    def cache_data(self) -> str:
        """The cache_data"""
        pass

    @cache_data.setter
    @abstractmethod
    def cache_data(self, new_value: str):
        """Setter for cache_data field"""
        pass

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        """The timestamp"""
        pass

    @timestamp.setter
    @abstractmethod
    def timestamp(self, new_value: datetime):
        """Setter for timestamp field"""
        pass

    @property
    @abstractmethod
    def cache_over_number(self) -> int:
        """The cache_over_number"""
        pass

    @cache_over_number.setter
    @abstractmethod
    def cache_over_number(self, new_value: int):
        """Setter for cache_over_number field"""
        pass
