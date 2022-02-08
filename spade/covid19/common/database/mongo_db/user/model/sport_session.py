import logging
from datetime import datetime
from typing import List, Optional

from mongoengine import Document

from covid19.common.database.mongo_db.models import User, SportSession, Exercise, ExerciseSet, DoneExercise
from covid19.common.database.mongo_db.user.model.done_exercise import MongoDBDoneExercise
from covid19.common.database.mongo_db.user.model.exercise_set import MongoDBExerciseSet
from covid19.common.database.user.field_enums import FunnyField
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession

logger = logging.getLogger(__name__)


class MongoDBSportSession(AbstractSportSession):
    """Actual implementation of SportSession on MongoDB"""

    def __init__(self, _parent_obj: Document, _sport_session_mongo_db_obj: SportSession):
        self._parent_obj: Document = _parent_obj
        self._sport_session_mongo_db_obj: SportSession = _sport_session_mongo_db_obj

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
    def exercise_set(self) -> MongoDBExerciseSet:
        exercise_set = self._sport_session_mongo_db_obj.exercise_set
        return MongoDBExerciseSet(exercise_set) if exercise_set else None

    @exercise_set.setter
    def exercise_set(self, new_value: AbstractExerciseSet):
        self._sport_session_mongo_db_obj.exercise_set = ExerciseSet.from_json(new_value.to_json_string())
        self._parent_obj.save()

    @property
    def started_at(self) -> datetime:
        return self._sport_session_mongo_db_obj.started_at

    @started_at.setter
    def started_at(self, new_value: datetime):
        self._sport_session_mongo_db_obj.started_at = new_value
        self._parent_obj.save()

    @property
    def ended_at(self) -> Optional[datetime]:
        return self._sport_session_mongo_db_obj.ended_at

    @ended_at.setter
    def ended_at(self, new_value: datetime):
        self._sport_session_mongo_db_obj.ended_at = new_value
        self._parent_obj.save()

    @property
    def aborted(self) -> bool:
        return self._sport_session_mongo_db_obj.aborted

    @aborted.setter
    def aborted(self, new_value: bool):
        self._sport_session_mongo_db_obj.aborted = new_value
        self._parent_obj.save()

    @property
    def done_exercises_ordered(self) -> List[MongoDBDoneExercise]:
        done_exercises_ordered = self._sport_session_mongo_db_obj.done_exercises_ordered
        return [
            MongoDBDoneExercise(self._parent_obj, done_exercise)
            for done_exercise in done_exercises_ordered
        ] if done_exercises_ordered else []

    def append_done_exercise(self, new_value: AbstractDoneExercise):
        to_add_done_exercise = DoneExercise.from_json(new_value.to_json_string())
        # NOTE: all reference fields should be "refreshed" from the string state, before inserting
        to_add_done_exercise.exercise = (
            Exercise.from_json(new_value.exercise.to_json_string())
        )
        self._sport_session_mongo_db_obj.done_exercises_ordered.append(to_add_done_exercise)
        self._parent_obj.save()

    @property
    def fun_rating(self) -> Optional[FunnyField]:
        fun_rating = self._sport_session_mongo_db_obj.fun_rating
        return FunnyField(fun_rating) if fun_rating else None

    @fun_rating.setter
    def fun_rating(self, new_value: FunnyField):
        self._sport_session_mongo_db_obj.fun_rating = new_value.value
        self._parent_obj.save()

    def to_json_string(self) -> str:
        return self._sport_session_mongo_db_obj.to_json()
