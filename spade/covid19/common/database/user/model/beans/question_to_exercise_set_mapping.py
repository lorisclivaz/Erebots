from dataclasses import dataclass
from typing import List, Optional

from bson import json_util

from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from covid19.common.database.user.field_enums import ShiftField, DifficultyField
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)


@dataclass
class QuestionToExerciseSetMappingBean(AbstractQuestionToExerciseSetMapping, ObjectWithIDBeanMixin):
    """A bean class to create mappings between questions an exercise sets, not directly bound to a database instance"""

    asked_question: Optional[AbstractEvaluationQuestion] = None
    user_answer: Optional[DifficultyField] = None
    question_shift: Optional[ShiftField] = None
    suitable_exercise_sets: Optional[List[AbstractExerciseSet]] = None

    def to_json_string(self) -> str:
        return json_util.dumps({
            'asked_question': self.asked_question.to_json() if self.asked_question else None,
            'user_answer': self.user_answer.value
            if self.user_answer is not None and self.user_answer.value in DifficultyField.values()
            else None,
            'question_shift': self.question_shift.value if self.question_shift else None,
            'suitable_exercise_sets': [
                goal.to_json() for goal in self.suitable_exercise_sets
            ] if self.suitable_exercise_sets else [],
        })
