import os

from mongoengine import connect, disconnect

from common.custom_chat.message_dao import AbstractMessageDAO
from common.database.mongo_db.cache.cache_dao import MongoDBCacheDAO
from covid19.common.database.connection_manager import AbstractCovid19ConnectionManager
from covid19.common.database.mongo_db.user.evaluation_question_dao import MongoDBEvaluationQuestionDAO
from covid19.common.database.mongo_db.user.exercise_dao import MongoDBExerciseDAO
from covid19.common.database.mongo_db.user.exercise_set_dao import MongoDBExerciseSetDAO
from covid19.common.database.mongo_db.user.question_to_exercise_set_mapping_dao import (
    MongoDBQuestionToExerciseSetMappingDAO
)
from common.database.mongo_db.persuation.strategy_dao import MongoDBStrategyDAO
from covid19.common.database.mongo_db.user.unread_message_dao import MongoDBUnreadMessageDAO
from covid19.common.database.mongo_db.user.user_dao import MongoDBUserDAO
from covid19.common.database.mongo_db.user.user_goal_dao import MongoDBUserGoalDAO
from covid19.common.database.user.model.abstract_user import AbstractUser

DATABASE_SERVER_IP = os.environ.get("DATABASE_SERVER_IP", "localhost")
"""The users Database server IP"""

DATABASE_SERVER_PORT = os.environ.get("DATABASE_SERVER_PORT", "27017")
"""The Database server port"""

DATABASE_SERVER_USERNAME = os.environ.get("DATABASE_SERVER_USERNAME", "root")
"""The Database server username"""

DATABASE_SERVER_PASSWORD = os.environ.get("DATABASE_SERVER_PASSWORD", "password")
"""The database server password"""

DATABASE_NAME = "covid19_db"
CONNECTION_URI = (f"mongodb://"
                  f"{DATABASE_SERVER_USERNAME}:{DATABASE_SERVER_PASSWORD}"
                  f"@{DATABASE_SERVER_IP}:{DATABASE_SERVER_PORT}/?authSource=admin")


class MongoDBConnectionManager(AbstractCovid19ConnectionManager):
    """Connection manager for MongoDB related to Covid19 project"""

    def __init__(self, database_name: str, database_uri: str, pryv_server_domain: str):
        super().__init__(database_name, database_uri)
        self._pryv_server_domain = pryv_server_domain

    def connect_to_db(self):
        return connect(self.database_name, host=self.database_uri)

    def disconnect_from_db(self):
        return disconnect()

    def get_user_dao(self) -> MongoDBUserDAO:
        return MongoDBUserDAO()

    def get_chat_messages_dao(self, user: AbstractUser) -> AbstractMessageDAO:
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def get_user_goal_dao(self) -> MongoDBUserGoalDAO:
        return MongoDBUserGoalDAO()

    def get_exercise_dao(self) -> MongoDBExerciseDAO:
        return MongoDBExerciseDAO()

    def get_exercise_set_dao(self) -> MongoDBExerciseSetDAO:
        return MongoDBExerciseSetDAO()

    def get_evaluation_question_dao(self) -> MongoDBEvaluationQuestionDAO:
        return MongoDBEvaluationQuestionDAO()

    def get_question_to_exercise_set_mapping_dao(self) -> MongoDBQuestionToExerciseSetMappingDAO:
        return MongoDBQuestionToExerciseSetMappingDAO()

    def get_unread_message_dao(self) -> MongoDBUnreadMessageDAO:
        return MongoDBUnreadMessageDAO()

    def get_cache_dao(self) -> MongoDBCacheDAO:
        return MongoDBCacheDAO()

    def get_strategy_dao(self) -> MongoDBStrategyDAO:
        return MongoDBStrategyDAO()

    def pryv_server_domain(self) -> str:
        return self._pryv_server_domain
