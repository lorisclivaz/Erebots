import logging
from datetime import datetime
from typing import Optional, Callable

from bson import json_util

from common.utils.dictionaries import remove_keys_with_none_values
from covid19.common.database.mongo_db.user.model.exercise import MongoDBExercise
from covid19.common.database.user.daos import AbstractExerciseDAO
from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_exercise import AbstractExercise

logger = logging.getLogger(__name__)


class PryvDoneExercise(AbstractDoneExercise):
    """Actual implementation of DoneExercise on Pryv"""

    def __init__(
            self,
            _referred_user_id: str,
            _done_exercise_json_obj: dict,
            _exercise_dao: AbstractExerciseDAO,
            _save_function: Callable[[], None]
    ):
        self._user_id: str = _referred_user_id
        self._done_exercise_json_obj: dict = _done_exercise_json_obj
        self._exercise_dao = _exercise_dao
        self._save_function = _save_function

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def exercise(self) -> Optional[MongoDBExercise]:
        exercise_id = self._done_exercise_json_obj.get('exercise', None)
        return self._exercise_dao.find_by_id(exercise_id) if exercise_id else None

    @exercise.setter
    def exercise(self, new_value: AbstractExercise):
        self._done_exercise_json_obj['exercise'] = {'$oid': new_value.id}
        self._save_function()

    @property
    def ended_at(self) -> Optional[datetime]:
        ended_at = self._done_exercise_json_obj.get('ended_at', None)
        return ended_at

    @ended_at.setter
    def ended_at(self, new_value: datetime):
        self._done_exercise_json_obj.ended_at = new_value
        self._save_function()

    @property
    def difficulty_rating(self) -> Optional[DifficultyField]:
        difficulty_rating = self._done_exercise_json_obj.get('difficulty_rating', None)
        difficulty_rating = (
            int(difficulty_rating) if isinstance(difficulty_rating, str) else difficulty_rating
        )
        return DifficultyField(difficulty_rating) if difficulty_rating in DifficultyField.values() else None

    @difficulty_rating.setter
    def difficulty_rating(self, new_value: DifficultyField):
        self._done_exercise_json_obj['difficulty_rating'] = new_value.value
        self._save_function()

    def to_json_string(self) -> str:
        return json_util.dumps(remove_keys_with_none_values(self._done_exercise_json_obj))
