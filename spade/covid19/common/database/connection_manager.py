from abc import ABC, abstractmethod

from common.custom_chat.message_dao import AbstractMessageDAO
from common.database.cache.abstract_cache_dao import AbstractCacheDAO
from common.database.connection_manager import AbstractConnectionManager
from common.database.persuation.dao import AbstractStrategyDAO
from covid19.common.database.user.daos import (
    AbstractExerciseDAO, AbstractExerciseSetDAO, AbstractUserDAO, AbstractUserGoalDAO, AbstractEvaluationQuestionDAO,
    AbstractQuestionToExerciseSetMappingDAO, AbstractUnreadMessageDAO
)
from covid19.common.database.user.model.abstract_user import AbstractUser


class AbstractCovid19ConnectionManager(AbstractConnectionManager, ABC):
    """A class to manage database connections related to Covid19 project"""

    @abstractmethod
    def get_user_dao(self) -> AbstractUserDAO:
        """Creates the User DAO for the actual database"""
        pass

    @abstractmethod
    def get_chat_messages_dao(self, user: AbstractUser) -> AbstractMessageDAO:
        """Creates the ChatMessages DAO for the actual database"""
        pass

    @abstractmethod
    def get_user_goal_dao(self) -> AbstractUserGoalDAO:
        """Creates the UserGoal DAO for the actual database"""
        pass

    @abstractmethod
    def get_exercise_dao(self) -> AbstractExerciseDAO:
        """Creates the Exercise DAO for the actual database"""
        pass

    @abstractmethod
    def get_exercise_set_dao(self) -> AbstractExerciseSetDAO:
        """Creates the ExerciseSet DAO for the actual database"""
        pass

    @abstractmethod
    def get_evaluation_question_dao(self) -> AbstractEvaluationQuestionDAO:
        """Creates the EvaluationQuestion DAO for the actual database"""
        pass

    @abstractmethod
    def get_question_to_exercise_set_mapping_dao(self) -> AbstractQuestionToExerciseSetMappingDAO:
        """Creates the QuestionToExerciseSetMapping DAO for the actual database"""
        pass

    @abstractmethod
    def get_unread_message_dao(self) -> AbstractUnreadMessageDAO:
        """Creates the UnreadMessage DAO for the actual database"""
        pass

    @abstractmethod
    def get_cache_dao(self) -> AbstractCacheDAO:
        """Retrieves the Cache data access object for the actual database"""
        pass

    @abstractmethod
    def get_strategy_dao(self) -> AbstractStrategyDAO:
        """Creates the Strategy DAO for the actual database"""
        pass

    @property
    @abstractmethod
    def pryv_server_domain(self) -> str:
        """Retrieves the Pryv server domain"""
        pass
