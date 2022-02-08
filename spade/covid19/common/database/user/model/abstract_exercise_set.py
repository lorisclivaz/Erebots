from abc import ABC, abstractmethod
from typing import List

from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible
from covid19.common.database.user.model.abstract_exercise import AbstractExercise
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


class AbstractExerciseSet(AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing a user goal"""

    @property
    @abstractmethod
    def exercise_list(self) -> List[AbstractExercise]:
        """Returns all exercises included in this set"""
        pass

    @exercise_list.setter
    @abstractmethod
    def exercise_list(self, new_value: List[AbstractExercise]):
        """Setter for exercise_list field"""
        pass

    @property
    @abstractmethod
    def suitable_for_goals(self) -> List[AbstractUserGoal]:
        """List of user goals for which this set of exercises is suitable"""
        pass

    @suitable_for_goals.setter
    @abstractmethod
    def suitable_for_goals(self, new_value: List[AbstractUserGoal]):
        """Setter for suitable_for_goals field"""
        pass
