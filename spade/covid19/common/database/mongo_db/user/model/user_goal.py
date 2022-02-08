from common.database.mongo_db.localized_object_mixin import MongoDBLocalizedObjectMixin
from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from covid19.common.database.mongo_db.models import UserGoal
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


class MongoDBUserGoal(AbstractUserGoal, MongoDBLocalizedObjectMixin, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractUserGoal for MongoDB"""

    def __init__(self, _mongo_db_obj: UserGoal):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        MongoDBLocalizedObjectMixin.__init__(self, _mongo_db_obj)
        self._user_goal_mongodb_obj: UserGoal = _mongo_db_obj

    def to_json_string(self) -> str:
        return self._user_goal_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, user_goal_json: str):
        """Creates a MongoDBUserGoal from a json string"""

        return cls(UserGoal.from_json(user_goal_json))
