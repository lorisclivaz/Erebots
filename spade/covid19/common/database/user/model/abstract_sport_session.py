from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from common.database.json_convertible import AbstractJsonConvertible
from covid19.common.database.user.field_enums import FunnyField
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet


class AbstractSportSession(AbstractJsonConvertible, ABC):
    """An abstract model representing a user SportSession"""

    @property
    @abstractmethod
    def user_id(self) -> str:
        """The SportSession referred user"""
        pass

    @property
    @abstractmethod
    def exercise_set(self) -> AbstractExerciseSet:
        """The sport-session exercise set field"""
        pass

    @exercise_set.setter
    @abstractmethod
    def exercise_set(self, new_value: AbstractExerciseSet):
        """Setter for exercise_set field"""
        pass

    @property
    @abstractmethod
    def started_at(self) -> datetime:
        """The sport session started_at field"""
        pass

    @started_at.setter
    @abstractmethod
    def started_at(self, new_value: datetime):
        """Setter for started_at field"""
        pass

    @property
    @abstractmethod
    def ended_at(self) -> Optional[datetime]:
        """The sport session ended_at field"""
        pass

    @ended_at.setter
    @abstractmethod
    def ended_at(self, new_value: datetime):
        """Setter for ended_at field"""
        pass

    @property
    @abstractmethod
    def aborted(self) -> bool:
        """Whether the sport session was aborted or not"""
        pass

    @aborted.setter
    @abstractmethod
    def aborted(self, new_value: bool):
        """Setter for aborted field"""
        pass

    @property
    @abstractmethod
    def done_exercises_ordered(self) -> List[AbstractDoneExercise]:
        """The user done_exercises_ordered"""
        pass

    @abstractmethod
    def append_done_exercise(self, new_value: AbstractDoneExercise):
        """Adds the newly provided done exercise to the user ones"""
        pass

    @property
    @abstractmethod
    def fun_rating(self) -> Optional[FunnyField]:
        """The user fun evaluation of done exercise set"""
        pass

    @fun_rating.setter
    @abstractmethod
    def fun_rating(self, new_value: FunnyField):
        """Setter for fun_rating field"""

    def __str__(self):
        try:
            return f"user_id: {self.user_id}, {self.to_json_string()}"
        except TypeError:
            return self.to_json_string()
