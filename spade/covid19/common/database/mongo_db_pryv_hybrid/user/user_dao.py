import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from covid19.common.database.mongo_db_pryv_hybrid.models import User
from covid19.common.database.mongo_db_pryv_hybrid.user.model.user import MongoDBAndPryvUser
from covid19.common.database.user.daos import (
    AbstractUserDAO, AbstractUserGoalDAO, AbstractEvaluationQuestionDAO, AbstractExerciseDAO, AbstractExerciseSetDAO
)
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class MongoDBAndPryvUserDAO(AbstractUserDAO, MongoDBDAOMixin[MongoDBAndPryvUser]):
    """Actual implementation for mongoDB and Pryv of the User Data Access Object"""

    def __init__(
            self,
            pryv_server_domain: str,
            user_goal_dao: AbstractUserGoalDAO,
            questions_dao: AbstractEvaluationQuestionDAO,
            exercise_dao: AbstractExerciseDAO,
            exercise_set_dao: AbstractExerciseSetDAO,
    ):
        MongoDBDAOMixin.__init__(self, User)
        self.pryv_server_domain = pryv_server_domain
        self._user_goal_dao = user_goal_dao
        self._questions_dao = questions_dao
        self._exercise_dao = exercise_dao
        self._exercise_set_dao = exercise_set_dao

    def wrap_mongo_db_object(self, mongo_db_object: User) -> MongoDBAndPryvUser:
        return MongoDBAndPryvUser(
            mongo_db_object,
            self.pryv_server_domain,
            self._user_goal_dao,
            self._questions_dao,
            self._exercise_dao,
            self._exercise_set_dao,
        )

    def insert(self, new_user: AbstractUser) -> AbstractUser:
        to_insert_user = User.from_json(new_user.to_json_string())
        to_insert_user.save()

        if (new_user.goals or new_user.sport_sessions or new_user.age or new_user.sex or new_user.current_question or
                new_user.current_question_answer or new_user.favourite_sport_days):
            logger.warning(f"No field except for 'pryv_endpoint' and 'telegram_id' will be saved")

        mongo_user = MongoDBAndPryvUser(
            to_insert_user,
            self.pryv_server_domain,
            self._user_goal_dao,
            self._questions_dao,
            self._exercise_dao,
            self._exercise_set_dao,
        )
        return mongo_user
