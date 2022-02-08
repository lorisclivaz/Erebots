import logging
from datetime import datetime
from typing import List, Optional

from bson import json_util

from common.pryv.api_wrapper import PryvAPI
from common.utils.dictionaries import remove_keys_with_none_values
from covid19.common.database.mongo_db_pryv_hybrid.user.model.done_exercise import PryvDoneExercise
from covid19.common.database.user.daos import AbstractExerciseSetDAO, AbstractExerciseDAO
from covid19.common.database.user.field_enums import FunnyField
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession

logger = logging.getLogger(__name__)


class PryvSportSession(AbstractSportSession):
    """Actual implementation of SportSession on Pryv"""

    def __init__(
            self,
            _referred_user_id: str,
            _sport_session_json_obj: dict,
            _sport_session_pryv_event_id: str,
            _pryv_api: PryvAPI,
            _user_api_endpoint_with_token: str,
            _exercise_dao: AbstractExerciseDAO,
            _exercise_set_dao: AbstractExerciseSetDAO,
    ):
        self._user_id: str = _referred_user_id
        self._sport_session_json_obj: dict = _sport_session_json_obj
        self._sport_session_pryv_event_id: str = _sport_session_pryv_event_id
        self._pryv_api = _pryv_api
        self._user_api_endpoint_with_token = _user_api_endpoint_with_token
        self._exercise_dao = _exercise_dao
        self._exercise_set_dao = _exercise_set_dao

    def _save_changes_to_event_in_pryv(self):
        """Utility function to save changes to that event in Pryv"""

        PryvAPI.save_changes_to_event(
            self._pryv_api, self._user_api_endpoint_with_token, self._sport_session_pryv_event_id,
            self._sport_session_json_obj
        )

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def exercise_set(self) -> AbstractExerciseSet:
        exercise_set_id = self._sport_session_json_obj.get('exercise_set', None)
        return self._exercise_set_dao.find_by_id(exercise_set_id) if exercise_set_id else None

    @exercise_set.setter
    def exercise_set(self, new_value: AbstractExerciseSet):
        self._sport_session_json_obj['exercise_set'] = {'$oid': new_value.id}
        self._save_changes_to_event_in_pryv()

    @property
    def started_at(self) -> datetime:
        started_at = self._sport_session_json_obj.get('started_at', None)
        return started_at

    @started_at.setter
    def started_at(self, new_value: datetime):
        self._sport_session_json_obj['started_at'] = new_value
        self._save_changes_to_event_in_pryv()

    @property
    def ended_at(self) -> Optional[datetime]:
        ended_at = self._sport_session_json_obj.get('ended_at', None)
        return ended_at

    @ended_at.setter
    def ended_at(self, new_value: datetime):
        self._sport_session_json_obj['ended_at'] = new_value
        self._save_changes_to_event_in_pryv()

    @property
    def aborted(self) -> bool:
        return self._sport_session_json_obj.get('aborted', False)

    @aborted.setter
    def aborted(self, new_value: bool):
        self._sport_session_json_obj['aborted'] = new_value
        self._save_changes_to_event_in_pryv()

    @property
    def done_exercises_ordered(self) -> List[PryvDoneExercise]:
        done_exercises_ordered = self._sport_session_json_obj.get('done_exercises_ordered', [])
        return [
            PryvDoneExercise(self._user_id, done_exercise, self._exercise_dao, self._save_changes_to_event_in_pryv)
            for done_exercise in done_exercises_ordered
        ] if done_exercises_ordered else []

    def append_done_exercise(self, new_value: AbstractDoneExercise):
        new_list = self._sport_session_json_obj.get('done_exercises_ordered', [])
        new_done_exercise = dict(new_value.to_json())

        # Replace actual instance of exercise set with its reference
        new_done_exercise['exercise'] = {'$oid': new_value.exercise.id}
        new_list.append(new_done_exercise)

        self._sport_session_json_obj['done_exercises_ordered'] = new_list
        self._save_changes_to_event_in_pryv()

    @property
    def fun_rating(self) -> Optional[FunnyField]:
        fun_rating = self._sport_session_json_obj.get('fun_rating', None)
        return FunnyField(fun_rating) if fun_rating else None

    @fun_rating.setter
    def fun_rating(self, new_value: FunnyField):
        self._sport_session_json_obj['fun_rating'] = new_value.value
        self._save_changes_to_event_in_pryv()

    def to_json_string(self) -> str:
        return json_util.dumps(remove_keys_with_none_values(self._sport_session_json_obj))
