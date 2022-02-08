from typing import Optional, List

from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from common.database.mongo_db.user.user_mixin import MongoDBUserMixin
from covid19.common.database.enums import AgeField, SexField, WeekDayField
from covid19.common.database.mongo_db.models import (
    User, UserGoal, SportSession, EvaluationQuestion, ExerciseSet
)
from covid19.common.database.mongo_db.user.model.evaluation_question import MongoDBEvaluationQuestion
from covid19.common.database.mongo_db.user.model.sport_session import MongoDBSportSession
from covid19.common.database.mongo_db.user.model.user_goal import MongoDBUserGoal
from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_chat_message import AbstractChatMessage
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


class MongoDBUser(AbstractUser, MongoDBUserMixin, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractUser for MongoDB"""

    def __init__(self, _mongo_db_obj: User):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        MongoDBUserMixin.__init__(self, _mongo_db_obj)
        self._user_mongodb_obj: User = _mongo_db_obj

    @property
    def age(self) -> Optional[AgeField]:
        age = self._user_mongodb_obj.age
        return AgeField(age) if age else None

    @age.setter
    def age(self, new_value: AgeField):
        self._user_mongodb_obj.age = new_value.value
        self._user_mongodb_obj.save()

    @property
    def sex(self) -> Optional[SexField]:
        sex = self._user_mongodb_obj.sex
        return SexField(sex) if sex else None

    @sex.setter
    def sex(self, new_value: SexField):
        self._user_mongodb_obj.sex = new_value.value
        self._user_mongodb_obj.save()

    @property
    def favourite_sport_days(self) -> List[WeekDayField]:
        favourite_sport_days = self._user_mongodb_obj.favourite_sport_days
        return [WeekDayField(weekday) for weekday in favourite_sport_days] if favourite_sport_days else []

    @favourite_sport_days.setter
    def favourite_sport_days(self, new_values: List[WeekDayField]):
        self._user_mongodb_obj.favourite_sport_days = [new_value.value for new_value in new_values]
        self._user_mongodb_obj.save()

    @property
    def goals(self) -> List[MongoDBUserGoal]:
        goals = self._user_mongodb_obj.goals
        return [MongoDBUserGoal(goal) for goal in goals] if goals else []

    @goals.setter
    def goals(self, new_values: List[AbstractUserGoal]):
        self._user_mongodb_obj.goals = [
            UserGoal.from_json(new_value.to_json_string()) for new_value in new_values
        ]
        self._user_mongodb_obj.save()

    @property
    def current_question(self) -> Optional[MongoDBEvaluationQuestion]:
        return (
            MongoDBEvaluationQuestion(self._user_mongodb_obj.current_question)
            if self._user_mongodb_obj.current_question else None
        )

    @current_question.setter
    def current_question(self, new_values: AbstractEvaluationQuestion):
        self._user_mongodb_obj.current_question = EvaluationQuestion.from_json(
            new_values.to_json_string()
        )
        self._user_mongodb_obj.save()

    @property
    def current_question_answer(self) -> Optional[DifficultyField]:
        current_question_answer = self._user_mongodb_obj.current_question_answer
        return DifficultyField(current_question_answer) if current_question_answer in DifficultyField.values() else None

    @current_question_answer.setter
    def current_question_answer(self, new_value: DifficultyField):
        self._user_mongodb_obj.current_question_answer = new_value.value
        self._user_mongodb_obj.save()

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
    def sport_sessions(self) -> List[MongoDBSportSession]:
        sport_sessions = self._user_mongodb_obj.sport_sessions
        return [
            MongoDBSportSession(self._user_mongodb_obj, sport_session)
            for sport_session in sport_sessions
        ] if sport_sessions else []

    def append_sport_session(self, new_value: AbstractSportSession):
        to_add_sport_session = SportSession.from_json(new_value.to_json_string())
        # NOTE: all reference fields should be "refreshed" from the string state, before inserting
        to_add_sport_session.exercise_set = ExerciseSet.from_json(new_value.exercise_set.to_json_string())

        to_add_sport_session.done_exercises_ordered = []
        mongo_sport_session = MongoDBSportSession(self._user_mongodb_obj, to_add_sport_session)
        for done_exercise in new_value.done_exercises_ordered:
            mongo_sport_session.append_done_exercise(done_exercise)

        self._user_mongodb_obj.sport_sessions.append(to_add_sport_session)
        self._user_mongodb_obj.save()

    @property
    def chat_messages(self) -> List[AbstractChatMessage]:
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def append_chat_message(self, new_value: AbstractChatMessage):
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def replace_chat_message(self, obj_id: str, new_value: AbstractChatMessage):
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def delete_chat_message(self, obj_id: str):
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def to_json_string(self) -> str:
        return self._user_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, user_json: str):
        """Creates a MongoDBUser from a json string"""

        return cls(User.from_json(user_json))
