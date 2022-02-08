from typing import List, Optional

from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from covid19.common.database.mongo_db.models import (
    QuestionToExerciseSetMapping, EvaluationQuestion, ExerciseSet
)
from covid19.common.database.mongo_db.user.model.evaluation_question import MongoDBEvaluationQuestion
from covid19.common.database.mongo_db.user.model.exercise_set import MongoDBExerciseSet
from covid19.common.database.user.field_enums import ShiftField, DifficultyField
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)


class MongoDBQuestionToExerciseSetMapping(AbstractQuestionToExerciseSetMapping, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractQuestionToExerciseSetMapping for MongoDB"""

    def __init__(self, _mongo_db_obj: QuestionToExerciseSetMapping):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        self._question_to_exercise_set_mapping_mongodb_obj: QuestionToExerciseSetMapping = _mongo_db_obj

    @property
    def asked_question(self) -> Optional[MongoDBEvaluationQuestion]:
        return (
            MongoDBEvaluationQuestion(self._question_to_exercise_set_mapping_mongodb_obj.asked_question)
            if self._question_to_exercise_set_mapping_mongodb_obj.asked_question else None
        )

    @asked_question.setter
    def asked_question(self, new_value: AbstractEvaluationQuestion):
        self._question_to_exercise_set_mapping_mongodb_obj.asked_question = EvaluationQuestion.from_json(
            new_value.to_json_string()
        )
        self._question_to_exercise_set_mapping_mongodb_obj.save()

    @property
    def user_answer(self) -> Optional[DifficultyField]:
        user_answer = self._question_to_exercise_set_mapping_mongodb_obj.user_answer
        return DifficultyField(user_answer) if user_answer in DifficultyField.values() else None

    @user_answer.setter
    def user_answer(self, new_value: DifficultyField):
        self._question_to_exercise_set_mapping_mongodb_obj.user_answer = new_value.value
        self._question_to_exercise_set_mapping_mongodb_obj.save()

    @property
    def question_shift(self) -> Optional[ShiftField]:
        question_shift = self._question_to_exercise_set_mapping_mongodb_obj.question_shift
        return ShiftField(question_shift) if question_shift else None

    @question_shift.setter
    def question_shift(self, new_value: Optional[ShiftField]):
        self._question_to_exercise_set_mapping_mongodb_obj.question_shift = new_value.value if new_value else None
        self._question_to_exercise_set_mapping_mongodb_obj.save()

    @property
    def suitable_exercise_sets(self) -> List[MongoDBExerciseSet]:
        suitable_exercise_sets = self._question_to_exercise_set_mapping_mongodb_obj.suitable_exercise_sets
        return [
            MongoDBExerciseSet(exercise_set) for exercise_set in suitable_exercise_sets
        ] if suitable_exercise_sets else []

    @suitable_exercise_sets.setter
    def suitable_exercise_sets(self, new_values: Optional[List[AbstractExerciseSet]]):
        self._question_to_exercise_set_mapping_mongodb_obj.suitable_exercise_sets = [
            ExerciseSet.from_json(new_value.to_json_string()) for new_value in new_values
        ] if new_values else None
        self._question_to_exercise_set_mapping_mongodb_obj.save()

    def to_json_string(self) -> str:
        return self._question_to_exercise_set_mapping_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, question_to_exercise_set_mapping_json: str):
        """Creates a MongoDBQuestionToExerciseSetMapping from a json string"""

        return cls(QuestionToExerciseSetMapping.from_json(question_to_exercise_set_mapping_json))
