from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from bson import json_util

from covid19.common.database.user.field_enums import FunnyField
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession


@dataclass
class SportSessionBean(AbstractSportSession):
    """A bean class to create sport sessions not directly bound to a database instance"""

    exercise_set: AbstractExerciseSet
    started_at: datetime
    ended_at: Optional[datetime] = None
    aborted: bool = False
    done_exercises_ordered: Optional[List[AbstractDoneExercise]] = None
    fun_rating: Optional[FunnyField] = None

    def user_id(self) -> str:
        raise RuntimeError(
            "A bean class doesn't have its parent ID set because it's assigned by the database, upon insert"
        )

    def exercise_set(self) -> AbstractExerciseSet:
        return self.exercise_set

    def started_at(self) -> datetime:
        return self.started_at

    def append_done_exercise(self, new_value: AbstractDoneExercise):
        self.done_exercises_ordered.append(new_value)

    def to_json_string(self) -> str:
        return json_util.dumps({
            'exercise_set': self.exercise_set.to_json() if self.exercise_set else None,
            'started_at': self.started_at,
            'ended_at': self.ended_at,
            'aborted': self.aborted,
            'done_exercises_ordered': [
                done_exercise.to_json() for done_exercise in self.done_exercises_ordered
            ] if self.done_exercises_ordered else [],
            'fun_rating': self.fun_rating.value if self.fun_rating else None,
        })
