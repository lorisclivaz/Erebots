import json
import logging
from typing import Optional, List, MutableMapping

from bson import json_util

from common.chat.language_enum import Language
from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from common.database.mongo_db.user.user_mixin import MongoDBUserMixin
from common.utils.dictionaries import remove_keys_with_none_values
from covid19.common.database.enums import AgeField, SexField, WeekDayField
from covid19.common.database.mongo_db.user.model.evaluation_question import MongoDBEvaluationQuestion
from covid19.common.database.mongo_db.user.model.user_goal import MongoDBUserGoal
from covid19.common.database.mongo_db_pryv_hybrid.models import User, PryvStoredData
from covid19.common.database.mongo_db_pryv_hybrid.user.model.chat_message import PryvChatMessage
from covid19.common.database.mongo_db_pryv_hybrid.user.model.sport_session import PryvSportSession
from covid19.common.database.user.daos import (
    AbstractUserGoalDAO, AbstractEvaluationQuestionDAO, AbstractExerciseSetDAO, AbstractExerciseDAO
)
from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_chat_message import AbstractChatMessage
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal
from common.pryv.api_wrapper import PryvAPI
from common.pryv.model import PryvEvent

logger = logging.getLogger(__name__)


class MongoDBAndPryvUser(AbstractUser, MongoDBUserMixin, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractUser for MongoDB and Pryv hybrid"""

    def __init__(
            self,
            _mongo_db_obj: User,
            _pryv_server_domain: str,
            _user_goal_dao: AbstractUserGoalDAO,
            _questions_dao: AbstractEvaluationQuestionDAO,
            _exercise_dao: AbstractExerciseDAO,
            _exercise_set_dao: AbstractExerciseSetDAO,
    ):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        MongoDBUserMixin.__init__(self, _mongo_db_obj)
        self._user_mongodb_obj: User = _mongo_db_obj
        self._pryv_api = PryvAPI(_pryv_server_domain)
        self._user_goal_dao = _user_goal_dao
        self._questions_dao = _questions_dao
        self._exercise_dao = _exercise_dao
        self._exercise_set_dao = _exercise_set_dao

        self._chat_message_id_to_pryv_event_id: MutableMapping[str, str] = {}

    def _access_pryv_stream_events_of(self, stream_id: str) -> List[PryvEvent]:
        """Utility method to access all the events in a Pryv stream"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            return self._pryv_api.get_events(user_endpoint_with_token, streams=[stream_id], sort_ascending=True)
        else:
            return []

    def _access_pryv_last_value_of(self, stream_id: str) -> Optional[str]:
        """Utility method to access the last value of a Pryv stream"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            stream_events = self._pryv_api.get_events(user_endpoint_with_token, streams=[stream_id], limit=1)
            return stream_events[0].content if stream_events else None
        else:
            return None

    def _set_pryv_new_value_for(self, stream_id: str, new_value: str, content_type: str = 'note/txt') -> \
            Optional[PryvEvent]:
        """Utility method to set a new event in a Pryv stream"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            return self._pryv_api.create_event(
                user_endpoint_with_token, [stream_id], new_value, content_type=content_type
            )
        else:
            logger.warning(f"Not setting value {new_value} for {stream_id},"
                           f" because the user has not a Pryv endpoint set.")

    @property
    def first_name(self) -> Optional[str]:
        first_name = self._access_pryv_last_value_of(PryvStoredData.FIRST_NAME.value[0])
        return first_name

    @first_name.setter
    def first_name(self, new_value: str):
        self._set_pryv_new_value_for(PryvStoredData.FIRST_NAME.value[0], new_value)

    # last_name is not here because not saved on pryv currently

    @property
    def language(self) -> Optional[Language]:
        language = self._access_pryv_last_value_of(PryvStoredData.LANGUAGE.value[0])
        return Language(language) if language else None

    @language.setter
    def language(self, new_value: Language):
        self._set_pryv_new_value_for(PryvStoredData.LANGUAGE.value[0], new_value.value)

    @property
    def age(self) -> Optional[AgeField]:
        age = self._access_pryv_last_value_of(PryvStoredData.AGE.value[0])
        return AgeField(age) if age else None

    @age.setter
    def age(self, new_value: AgeField):
        self._set_pryv_new_value_for(PryvStoredData.AGE.value[0], new_value.value)

    @property
    def sex(self) -> Optional[SexField]:
        sex = self._access_pryv_last_value_of(PryvStoredData.SEX.value[0])
        return SexField(sex) if sex else None

    @sex.setter
    def sex(self, new_value: SexField):
        self._set_pryv_new_value_for(PryvStoredData.SEX.value[0], new_value.value)

    @property
    def favourite_sport_days(self) -> List[WeekDayField]:
        favourite_sport_days = self._access_pryv_last_value_of(PryvStoredData.FAVOURITE_SPORT_DAYS.value[0])
        return [
            WeekDayField(weekday) for weekday in json_util.loads(favourite_sport_days)
        ] if favourite_sport_days else []

    @favourite_sport_days.setter
    def favourite_sport_days(self, new_values: List[WeekDayField]):
        self._set_pryv_new_value_for(
            PryvStoredData.FAVOURITE_SPORT_DAYS.value[0],
            json_util.dumps([new_value.value for new_value in new_values])
        )

    @property
    def goals(self) -> List[MongoDBUserGoal]:
        goal_ids = self._access_pryv_last_value_of(PryvStoredData.GOALS.value[0])
        return [self._user_goal_dao.find_by_id(goal_id) for goal_id in json_util.loads(goal_ids)] if goal_ids else []

    @goals.setter
    def goals(self, new_values: List[AbstractUserGoal]):
        new_goal_ids = [{'$oid': new_value.id} for new_value in new_values]
        self._set_pryv_new_value_for(PryvStoredData.GOALS.value[0], json_util.dumps(new_goal_ids))

    @property
    def current_question(self) -> Optional[MongoDBEvaluationQuestion]:
        question_id = self._access_pryv_last_value_of(PryvStoredData.CURRENT_QUESTION.value[0])
        return self._questions_dao.find_by_id(json_util.loads(question_id)) if question_id else None

    @current_question.setter
    def current_question(self, new_value: AbstractEvaluationQuestion):
        self._set_pryv_new_value_for(PryvStoredData.CURRENT_QUESTION.value[0], json_util.dumps({'$oid': new_value.id}))

    @property
    def current_question_answer(self) -> Optional[DifficultyField]:
        current_question_answer = self._access_pryv_last_value_of(PryvStoredData.CURRENT_QUESTION_ANSWER.value[0])
        current_question_answer = (
            int(current_question_answer) if isinstance(current_question_answer, str) else current_question_answer
        )
        return DifficultyField(current_question_answer) if current_question_answer in DifficultyField.values() else None

    @current_question_answer.setter
    def current_question_answer(self, new_value: DifficultyField):
        self._set_pryv_new_value_for(PryvStoredData.CURRENT_QUESTION_ANSWER.value[0], str(new_value.value))

    @property
    def telegram_id(self) -> Optional[str]:
        return self._user_mongodb_obj.telegram_id

    @telegram_id.setter
    def telegram_id(self, new_value: str):
        self._user_mongodb_obj.telegram_id = new_value
        self._user_mongodb_obj.save()

    @property
    def custom_chat_id(self) -> Optional[str]:
        return self._user_mongodb_obj.custom_chat_id

    @custom_chat_id.setter
    def custom_chat_id(self, new_value: str):
        self._user_mongodb_obj.custom_chat_id = new_value
        self._user_mongodb_obj.save()

    @property
    def pryv_endpoint(self) -> Optional[str]:
        return self._user_mongodb_obj.pryv_endpoint

    @pryv_endpoint.setter
    def pryv_endpoint(self, new_value: str):
        self._user_mongodb_obj.pryv_endpoint = new_value
        self._user_mongodb_obj.save()

    @property
    def registration_completed(self) -> bool:
        return self._user_mongodb_obj.registration_completed

    @registration_completed.setter
    def registration_completed(self, new_value: bool):
        self._user_mongodb_obj.registration_completed = new_value
        self._user_mongodb_obj.save()

    @property
    def sport_sessions(self) -> List[PryvSportSession]:
        sport_session_events = self._access_pryv_stream_events_of(PryvStoredData.SPORT_SESSIONS.value[0])
        return [
            PryvSportSession(
                self.id, json_util.loads(sport_session_event.content), sport_session_event.id, self._pryv_api,
                self._user_mongodb_obj.pryv_endpoint, self._exercise_dao, self._exercise_set_dao
            )
            for sport_session_event in sport_session_events
        ] if sport_session_events else []

    def append_sport_session(self, new_value: AbstractSportSession):
        sport_session_json = dict(new_value.to_json())

        # Replace actual instance of exercise set with its reference
        sport_session_json['exercise_set'] = {'$oid': new_value.exercise_set.id}
        self._set_pryv_new_value_for(
            PryvStoredData.SPORT_SESSIONS.value[0],
            json_util.dumps(remove_keys_with_none_values(sport_session_json))
        )

    @property
    def chat_messages(self) -> List[AbstractChatMessage]:
        chat_message_events = self._access_pryv_stream_events_of(PryvStoredData.CHAT_MESSAGES.value[0])
        result_messages = []
        self._chat_message_id_to_pryv_event_id = {}
        for chat_message_event in chat_message_events:
            chat_message = PryvChatMessage(
                self.id, json_util.loads(chat_message_event.content), chat_message_event.id, self._pryv_api,
                self._user_mongodb_obj.pryv_endpoint
            )
            result_messages.append(chat_message)
            self._chat_message_id_to_pryv_event_id[chat_message.message_id] = chat_message_event.id

        return result_messages

    def append_chat_message(self, new_value: AbstractChatMessage):
        created_event = self._set_pryv_new_value_for(
            PryvStoredData.CHAT_MESSAGES.value[0],
            json_util.dumps(remove_keys_with_none_values(dict(new_value.to_json())))
        )

        if created_event:
            self._chat_message_id_to_pryv_event_id[new_value.message_id] = created_event.id

    def replace_chat_message(self, message_id: str, new_value: AbstractChatMessage):
        pryv_event_id = self._chat_message_id_to_pryv_event_id[message_id]
        PryvAPI.save_changes_to_event(
            self._pryv_api, self._user_mongodb_obj.pryv_endpoint, pryv_event_id,
            new_value.payload
        )

    def delete_chat_message(self, message_id: str):
        pryv_event_id = self._chat_message_id_to_pryv_event_id[message_id]
        self._pryv_api.delete_event(self._user_mongodb_obj.pryv_endpoint, pryv_event_id)

    def to_json_string(self) -> str:
        mongo_db_json = json.loads(self._user_mongodb_obj.to_json())

        first_name = self.first_name
        last_name = self.last_name
        language = self.language
        age = self.age
        sex = self.sex
        favourite_sport_days = self.favourite_sport_days
        goals = self.goals
        current_question = self.current_question
        current_question_answer = self.current_question_answer
        sport_sessions = self.sport_sessions

        hybrid_json = {
            **mongo_db_json,
            'first_name': first_name,
            'last_name': last_name,
            'language': language.value if language else None,
            'age': age.value if age else None,
            'sex': sex.value if sex else None,
            'favourite_sport_days': [
                day.value for day in favourite_sport_days
            ] if favourite_sport_days else [],
            'goals': [{'$oid': goal.id} for goal in goals] if goals else [],
            'current_question': {'$oid': current_question.id} if current_question else None,
            'current_question_answer': (
                current_question_answer.value if (
                        current_question_answer is not None and
                        current_question_answer.value in DifficultyField.values()
                ) else None
            ),
            'sport_sessions': [
                sport_session.to_json() for sport_session in sport_sessions
            ] if sport_sessions else [],
        }
        return json_util.dumps(remove_keys_with_none_values(hybrid_json))
