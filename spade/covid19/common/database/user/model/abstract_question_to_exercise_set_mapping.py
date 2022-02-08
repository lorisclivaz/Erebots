from abc import ABC, abstractmethod
from typing import List, Optional

from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible
from covid19.common.database.user.field_enums import DifficultyField, ShiftField
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet


class AbstractQuestionToExerciseSetMapping(AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing a mapping between a question and its suitable exercise sets"""

    @property
    @abstractmethod
    def asked_question(self) -> Optional[AbstractEvaluationQuestion]:
        """The asked evaluation question"""
        pass

    @asked_question.setter
    @abstractmethod
    def asked_question(self, new_value: AbstractEvaluationQuestion):
        """Setter for asked_question field"""
        pass

    @property
    @abstractmethod
    def user_answer(self) -> Optional[DifficultyField]:
        """The user_answer"""
        pass

    @user_answer.setter
    @abstractmethod
    def user_answer(self, new_value: DifficultyField):
        """Setter for user_answer field"""
        pass

    @property
    @abstractmethod
    def question_shift(self) -> Optional[ShiftField]:
        """The question_shift to be done"""
        pass

    @question_shift.setter
    @abstractmethod
    def question_shift(self, new_value: Optional[ShiftField]):
        """Setter for question_shift field"""
        pass

    @property
    @abstractmethod
    def suitable_exercise_sets(self) -> Optional[List[AbstractExerciseSet]]:
        """Returns all suitable exercise sets for current question + answer pair"""
        pass

    @suitable_exercise_sets.setter
    @abstractmethod
    def suitable_exercise_sets(self, new_value: Optional[List[AbstractExerciseSet]]):
        """Setter for suitable_exercise_sets field"""
        pass
