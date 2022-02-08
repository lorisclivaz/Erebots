import os

from get_docker_secret import get_docker_secret
from mongoengine import connect, disconnect

from common.custom_chat.message_dao import AbstractMessageDAO
from common.database.mongo_db.cache.cache_dao import MongoDBCacheDAO
from echo.common.database.connection_manager import AbstractEchoConnectionManager
from echo.common.database.mongo_db.user.unread_message_dao import MongoDBUnreadMessageDAO
from echo.common.database.mongo_db.user.user_dao import MongoDBUserDAO
from echo.common.database.user.model.abstract_user import AbstractUser

DATABASE_SERVER_IP = os.environ.get("DATABASE_SERVER_IP", "localhost")
"""The users Database server IP"""

DATABASE_SERVER_PORT = os.environ.get("DATABASE_SERVER_PORT", "27017")
"""The Database server port"""

DATABASE_SERVER_USERNAME = os.environ.get("DATABASE_SERVER_USERNAME", "root")
"""The Database server username"""

DATABASE_SERVER_PASSWORD = get_docker_secret(
    'database_server_password', autocast_name=True, getenv=True, default='password',
    secrets_dir='/run/secrets'
)
"""The database server password"""

DATABASE_NAME = "echo_db"
CONNECTION_URI = (f"mongodb://"
                  f"{DATABASE_SERVER_USERNAME}:{DATABASE_SERVER_PASSWORD}"
                  f"@{DATABASE_SERVER_IP}:{DATABASE_SERVER_PORT}/?authSource=admin")


class MongoDBConnectionManager(AbstractEchoConnectionManager):
    """Connection manager for MongoDB related to echo project"""

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

    def get_unread_message_dao(self) -> MongoDBUnreadMessageDAO:
        return MongoDBUnreadMessageDAO()

    def get_cache_dao(self) -> MongoDBCacheDAO:
        return MongoDBCacheDAO()

    def pryv_server_domain(self) -> str:
        return self._pryv_server_domain
