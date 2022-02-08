import json
from dataclasses import dataclass
from typing import Optional, List

from bson import json_util

from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from common.database.user.beans.user_bean_mixin import BasicUserBeanMixin
from covid19.common.database.enums import AgeField, SexField, WeekDayField
from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_chat_message import AbstractChatMessage
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


@dataclass
class UserBean(AbstractUser, BasicUserBeanMixin, ObjectWithIDBeanMixin):
    """A bean class to create users not directly bound to a database instance"""

    age: Optional[AgeField] = None
    sex: Optional[SexField] = None
    favourite_sport_days: Optional[List[WeekDayField]] = None
    goals: Optional[List[AbstractUserGoal]] = None
    current_question: Optional[AbstractEvaluationQuestion] = None
    current_question_answer: Optional[DifficultyField] = None
    telegram_id: Optional[str] = None
    custom_chat_id: Optional[str] = None
    pryv_endpoint: Optional[str] = None
    registration_completed: bool = False
    sport_sessions: Optional[List[AbstractSportSession]] = None
    chat_messages: Optional[List[AbstractChatMessage]] = None

    def append_sport_session(self, new_value: AbstractSportSession):
        self.sport_sessions.append(new_value)

    def append_chat_message(self, new_value: AbstractChatMessage):
        self.chat_messages.append(new_value)

    def replace_chat_message(self, obj_id: str, new_value: AbstractChatMessage):
        self.chat_messages = [obj if obj.message_id != obj_id else new_value
                              for obj in self.chat_messages]

    def delete_chat_message(self, obj_id: str):
        self.chat_messages = [obj for obj in self.chat_messages
                              if obj.message_id != obj_id]

    def to_json_string(self) -> str:
        return json_util.dumps({
            **json.loads(BasicUserBeanMixin.to_json_string(self)),
            'age': self.age.value if self.age else None,
            'sex': self.sex.value if self.sex else None,
            'favourite_sport_days': [
                day.value for day in self.favourite_sport_days
            ] if self.favourite_sport_days else [],
            'goals': [goal.to_json() for goal in self.goals] if self.goals else [],
            'current_question': self.current_question.to_json() if self.current_question else None,
            'current_question_answer': (
                self.current_question_answer.value if (
                        self.current_question_answer is not None and
                        self.current_question_answer.value in DifficultyField.values()
                ) else None
            ),
            'telegram_id': self.telegram_id,
            'custom_chat_id': self.custom_chat_id,
            'pryv_endpoint': self.pryv_endpoint,
            'registration_completed': self.registration_completed,
            'sport_sessions': [
                sport_session.to_json() for sport_session in self.sport_sessions
            ] if self.sport_sessions else [],
            'chat_messages': [
                chat_message.to_json() for chat_message in self.chat_messages
            ] if self.chat_messages else [],
        })
