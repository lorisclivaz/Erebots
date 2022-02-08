import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from echo.common.database.mongo_db_pryv_hybrid.models import User
from echo.common.database.mongo_db_pryv_hybrid.user.model.user import MongoDBAndPryvUser
from echo.common.database.user.daos import AbstractUserDAO
from echo.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class MongoDBAndPryvUserDAO(AbstractUserDAO, MongoDBDAOMixin[MongoDBAndPryvUser]):
    """Actual implementation for mongoDB and Pryv of the User Data Access Object"""

    def __init__(
            self,
            pryv_server_domain: str
    ):
        MongoDBDAOMixin.__init__(self, User)
        self.pryv_server_domain = pryv_server_domain

    def wrap_mongo_db_object(self, mongo_db_object: User) -> MongoDBAndPryvUser:
        return MongoDBAndPryvUser(
            mongo_db_object,
            self.pryv_server_domain
        )

    def insert(self, new_user: AbstractUser) -> AbstractUser:
        to_insert_user = User.from_json(new_user.to_json_string())
        to_insert_user.save()

        mongo_user = MongoDBAndPryvUser(
            to_insert_user,
            self.pryv_server_domain
        )
        return mongo_user
