from abc import ABC, abstractmethod
from typing import Optional, List

from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible
from common.database.user.abstract_user import AbstractBasicUser
from covid19.common.database.enums import AgeField, SexField, WeekDayField
from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_chat_message import AbstractChatMessage
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


class AbstractUser(AbstractBasicUser, AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing a user profile"""

    @property
    @abstractmethod
    def age(self) -> Optional[AgeField]:
        """The user age"""
        pass

    @age.setter
    @abstractmethod
    def age(self, new_value: AgeField):
        """Setter for age field"""
        pass

    @property
    @abstractmethod
    def sex(self) -> Optional[SexField]:
        """The user sex"""
        pass

    @sex.setter
    @abstractmethod
    def sex(self, new_value: SexField):
        """Setter for sex field"""
        pass

    @property
    @abstractmethod
    def favourite_sport_days(self) -> List[WeekDayField]:
        """The user favourite_sport_days"""
        pass

    @favourite_sport_days.setter
    @abstractmethod
    def favourite_sport_days(self, new_value: List[WeekDayField]):
        """Setter for favourite_sport_days field"""
        pass

    @property
    @abstractmethod
    def goals(self) -> List[AbstractUserGoal]:
        """The user goals"""
        pass

    @goals.setter
    @abstractmethod
    def goals(self, new_value: List[AbstractUserGoal]):
        """Setter for goals field"""
        pass

    @property
    @abstractmethod
    def current_question(self) -> Optional[AbstractEvaluationQuestion]:
        """The evaluation question at which the user is stuck"""
        pass

    @current_question.setter
    @abstractmethod
    def current_question(self, new_value: AbstractEvaluationQuestion):
        """Setter for current_question field"""
        pass

    @property
    @abstractmethod
    def current_question_answer(self) -> Optional[DifficultyField]:
        """The user response to current evaluation question"""
        pass

    @current_question_answer.setter
    @abstractmethod
    def current_question_answer(self, new_value: DifficultyField):
        """Setter for current_question_answer field"""
        pass

    @property
    @abstractmethod
    def telegram_id(self) -> Optional[str]:
        """The user telegram_id"""
        pass

    @telegram_id.setter
    @abstractmethod
    def telegram_id(self, new_value: str):
        """Setter for telegram_id field"""
        pass

    @property
    @abstractmethod
    def custom_chat_id(self) -> Optional[str]:
        """The user custom_chat_id"""
        pass

    @custom_chat_id.setter
    @abstractmethod
    def custom_chat_id(self, new_value: str):
        """Setter for custom_chat_id field"""
        pass

    @property
    @abstractmethod
    def pryv_endpoint(self) -> Optional[str]:
        """The user pryv_endpoint"""
        pass

    @pryv_endpoint.setter
    @abstractmethod
    def pryv_endpoint(self, new_value: str):
        """Setter for pryv_endpoint field"""
        pass

    @property
    @abstractmethod
    def registration_completed(self) -> bool:
        """Whether the user completed the registration process"""
        pass

    @registration_completed.setter
    @abstractmethod
    def registration_completed(self, new_value: bool):
        """Setter for registration_completed field"""
        pass

    @property
    @abstractmethod
    def sport_sessions(self) -> List[AbstractSportSession]:
        """The user sport_sessions"""
        pass

    @abstractmethod
    def append_sport_session(self, new_value: AbstractSportSession):
        """Adds the newly provided sport session to the user ones"""
        pass

    @property
    @abstractmethod
    def chat_messages(self) -> List[AbstractChatMessage]:
        """The user chat_messages"""
        pass

    @abstractmethod
    def append_chat_message(self, new_value: AbstractChatMessage):
        """Adds the newly provided chat_message to the user ones"""
        pass

    @abstractmethod
    def replace_chat_message(self, obj_id: str, new_value: AbstractChatMessage):
        """Replaces the message with provided id with the new one"""
        pass

    @abstractmethod
    def delete_chat_message(self, obj_id: str):
        """Deletes the message with provided id"""
        pass
