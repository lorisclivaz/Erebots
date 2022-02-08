from __future__ import annotations  # Needed in python 3.7 to have the current class type as a return type of methods

from abc import ABC, abstractmethod
from typing import Optional

from common.database.abstract_localized_object import AbstractLocalizedObject
from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible


class AbstractEvaluationQuestion(AbstractLocalizedObject, AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing an evaluation question"""

    @property
    @abstractmethod
    def next(self) -> Optional[AbstractEvaluationQuestion]:
        """The next evaluation question"""
        pass

    @next.setter
    @abstractmethod
    def next(self, new_value: Optional[AbstractEvaluationQuestion]):
        """Setter for next field"""
        pass

    @property
    @abstractmethod
    def previous(self) -> Optional[AbstractEvaluationQuestion]:
        """The previous evaluation question"""
        pass

    @previous.setter
    @abstractmethod
    def previous(self, new_value: Optional[AbstractEvaluationQuestion]):
        """Setter for previous field"""
        pass
