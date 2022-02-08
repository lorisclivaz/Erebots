from abc import ABC, abstractmethod
from typing import Optional

from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible


class AbstractStrategy(AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing a strategy"""

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """The strategy name"""
        pass

    @name.setter
    @abstractmethod
    def name(self, new_value: str):
        """Setter for label name"""
        pass

    @property
    @abstractmethod
    def description(self) -> Optional[str]:
        """The strategy description"""
        pass

    @description.setter
    @abstractmethod
    def description(self, new_value: str):
        """Setter for description name"""
        pass
