import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from covid19.common.database.mongo_db.models import (User, UserGoal, EvaluationQuestion)
from covid19.common.database.mongo_db.user.model.user import MongoDBUser
from covid19.common.database.user.daos import AbstractUserDAO
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class MongoDBUserDAO(AbstractUserDAO, MongoDBDAOMixin[MongoDBUser]):
    """Actual implementation for mongoDB of the User Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, User)

    def wrap_mongo_db_object(self, mongo_db_object: User) -> MongoDBUser:
        return MongoDBUser(mongo_db_object)

    def insert(self, new_user: AbstractUser) -> AbstractUser:
        to_insert_user = User.from_json(new_user.to_json_string())

        # NOTE: all reference fields should be "refreshed" from the string state, before inserting
        to_insert_user.goals = [UserGoal.from_json(goal.to_json_string()) for goal in new_user.goals]
        to_insert_user.current_question = (
            EvaluationQuestion.from_json(new_user.current_question.to_json_string())
            if new_user.current_question else None
        )

        to_insert_user.sport_sessions = []
        to_insert_user.save()

        # Now deeper structures insertion
        mongo_user = MongoDBUser(to_insert_user)

        if new_user.sport_sessions:
            for sport_session in new_user.sport_sessions:
                mongo_user.append_sport_session(sport_session)

        return mongo_user
