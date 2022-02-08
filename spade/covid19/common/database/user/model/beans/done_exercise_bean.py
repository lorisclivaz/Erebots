from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bson import json_util

from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_exercise import AbstractExercise


@dataclass
class DoneExerciseBean(AbstractDoneExercise):
    """A bean class to create done exercises not directly bound to a database instance"""

    exercise: AbstractExercise
    ended_at: Optional[datetime] = None
    difficulty_rating: Optional[DifficultyField] = None

    def user_id(self) -> str:
        raise RuntimeError(
            "A bean class doesn't have its parent ID set because it's assigned by the database, upon insert"
        )

    def exercise(self) -> AbstractExercise:
        return self.exercise

    def to_json_string(self) -> str:
        return json_util.dumps({
            'exercise': self.exercise.to_json() if self.exercise else None,
            'ended_at': self.ended_at,
            'difficulty_rating': (
                self.difficulty_rating.value
                if self.difficulty_rating is not None and self.difficulty_rating.value in DifficultyField.values()
                else None
            ),
        })
