from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from common.database.json_convertible import AbstractJsonConvertible
from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_exercise import AbstractExercise


class AbstractDoneExercise(AbstractJsonConvertible, ABC):
    """An abstract model representing a user DoneExercise"""

    @property
    @abstractmethod
    def user_id(self) -> str:
        """The DoneExercise referred user"""
        pass

    @property
    @abstractmethod
    def exercise(self) -> AbstractExercise:
        """The suggestion event exercise field"""
        pass

    @exercise.setter
    @abstractmethod
    def exercise(self, new_value: AbstractExercise):
        """Setter for exercise field"""
        pass

    @property
    @abstractmethod
    def ended_at(self) -> Optional[datetime]:
        """The done exercise ended_at field"""
        pass

    @ended_at.setter
    @abstractmethod
    def ended_at(self, new_value: datetime):
        """Setter for ended_at field"""
        pass

    @property
    @abstractmethod
    def difficulty_rating(self) -> Optional[DifficultyField]:
        """The user evaluation of current exercise difficulty"""
        pass

    @difficulty_rating.setter
    @abstractmethod
    def difficulty_rating(self, new_value: DifficultyField):
        """Setter for difficulty_rating field"""
        pass

    def __str__(self):
        try:
            return f"user_id: {self.user_id}, {self.to_json_string()}"
        except TypeError:
            return self.to_json_string()
