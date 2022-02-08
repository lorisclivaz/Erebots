import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from covid19.common.database.mongo_db.models import UserGoal
from covid19.common.database.mongo_db.user.model.user_goal import MongoDBUserGoal
from covid19.common.database.user.daos import AbstractUserGoalDAO
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal

logger = logging.getLogger(__name__)


class MongoDBUserGoalDAO(AbstractUserGoalDAO, MongoDBDAOMixin[MongoDBUserGoal]):
    """Actual implementation for mongoDB of the UserGoal Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, UserGoal)

    def wrap_mongo_db_object(self, mongo_db_object: UserGoal) -> MongoDBUserGoal:
        return MongoDBUserGoal(mongo_db_object)

    def insert(self, new_user_goal: AbstractUserGoal) -> AbstractUserGoal:
        to_insert_user_goal = UserGoal.from_json(new_user_goal.to_json_string())
        to_insert_user_goal.save()
        return MongoDBUserGoal(to_insert_user_goal)
