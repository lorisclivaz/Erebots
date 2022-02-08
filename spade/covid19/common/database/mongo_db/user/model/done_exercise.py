import logging
from datetime import datetime
from typing import Optional

from mongoengine import Document

from covid19.common.database.mongo_db.models import User, Exercise, DoneExercise
from covid19.common.database.mongo_db.user.model.exercise import MongoDBExercise
from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_exercise import AbstractExercise

logger = logging.getLogger(__name__)


class MongoDBDoneExercise(AbstractDoneExercise):
    """Actual implementation of DoneExercise on MongoDB"""

    def __init__(self, _parent_obj: Document, _done_exercise_mongo_db_obj: DoneExercise):
        self._parent_obj: Document = _parent_obj
        self._done_exercise_mongo_db_obj: DoneExercise = _done_exercise_mongo_db_obj

    @property
    def user_id(self) -> str:
        if isinstance(self._parent_obj, User):
            user_obj: User = self._parent_obj
            return str(user_obj.id)
        else:
            error_message = (f" The type of parent obj is not as expected! "
                             f"Expected: `User`, Actual: `{self._parent_obj}`")
            logger.error(error_message)
            raise TypeError(error_message)

    @property
    def exercise(self) -> Optional[MongoDBExercise]:
        return (
            MongoDBExercise(self._done_exercise_mongo_db_obj.exercise)
            if self._done_exercise_mongo_db_obj.exercise else None
        )

    @exercise.setter
    def exercise(self, new_value: AbstractExercise):
        self._done_exercise_mongo_db_obj.exercise = Exercise.from_json(
            new_value.to_json_string()
        )
        self._parent_obj.save()

    @property
    def ended_at(self) -> Optional[datetime]:
        return self._done_exercise_mongo_db_obj.ended_at

    @ended_at.setter
    def ended_at(self, new_value: datetime):
        self._done_exercise_mongo_db_obj.ended_at = new_value
        self._parent_obj.save()

    @property
    def difficulty_rating(self) -> Optional[DifficultyField]:
        difficulty_rating = self._done_exercise_mongo_db_obj.difficulty_rating
        return DifficultyField(difficulty_rating) if difficulty_rating in DifficultyField.values() else None

    @difficulty_rating.setter
    def difficulty_rating(self, new_value: DifficultyField):
        self._done_exercise_mongo_db_obj.difficulty_rating = new_value.value
        self._parent_obj.save()

    def to_json_string(self) -> str:
        return self._done_exercise_mongo_db_obj.to_json()
