from abc import ABC, abstractmethod
from typing import Optional

from common.database.abstract_localized_object import AbstractLocalizedObject
from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible


class AbstractExercise(AbstractLocalizedObject, AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing an exercise"""

    @property
    @abstractmethod
    def label(self) -> Optional[str]:
        """The exercise mnemonic label"""
        pass

    @label.setter
    @abstractmethod
    def label(self, new_value: str):
        """Setter for label field"""
        pass

    @property
    @abstractmethod
    def gif_path(self) -> Optional[str]:
        """The exercise GIF path"""
        pass

    @gif_path.setter
    @abstractmethod
    def gif_path(self, new_value: str):
        """Setter for gif_path field"""
        pass
