import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from echo.common.database.mongo_db.models import User
from echo.common.database.mongo_db.user.model.user import MongoDBUser
from echo.common.database.user.daos import AbstractUserDAO
from echo.common.database.user.model.abstract_user import AbstractUser

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
        to_insert_user.save()

        # Now deeper structures insertion
        mongo_user = MongoDBUser(to_insert_user)

        return mongo_user
