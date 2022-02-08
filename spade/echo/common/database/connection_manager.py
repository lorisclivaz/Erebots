from abc import ABC, abstractmethod

from common.custom_chat.message_dao import AbstractMessageDAO
from common.database.cache.abstract_cache_dao import AbstractCacheDAO
from common.database.connection_manager import AbstractConnectionManager
from echo.common.database.user.daos import (
    AbstractUserDAO, AbstractUnreadMessageDAO
)
from echo.common.database.user.model.abstract_user import AbstractUser


class AbstractEchoConnectionManager(AbstractConnectionManager, ABC):
    """A class to manage database connections related to echo project"""

    @abstractmethod
    def get_user_dao(self) -> AbstractUserDAO:
        """Creates the User DAO for the actual database"""
        pass

    @abstractmethod
    def get_chat_messages_dao(self, user: AbstractUser) -> AbstractMessageDAO:
        """Creates the ChatMessages DAO for the actual database"""
        pass

    @abstractmethod
    def get_unread_message_dao(self) -> AbstractUnreadMessageDAO:
        """Creates the UnreadMessage DAO for the actual database"""
        pass

    @abstractmethod
    def get_cache_dao(self) -> AbstractCacheDAO:
        """Retrieves the Cache data access object for the actual database"""
        pass

    @property
    @abstractmethod
    def pryv_server_domain(self) -> str:
        """Retrieves the Pryv server domain"""
        pass
