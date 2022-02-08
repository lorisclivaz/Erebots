from abc import ABC

from common.database.abstract_dao import AbstractDAO
from echo.common.database.user.model.abstract_unread_message import AbstractUnreadMessage
from echo.common.database.user.model.abstract_user import AbstractUser


class AbstractUserDAO(AbstractDAO[AbstractUser], ABC):
    """A base class to implement Data Access Object for User"""
    pass


class AbstractUnreadMessageDAO(AbstractDAO[AbstractUnreadMessage], ABC):
    """A base class to implement Data Access Object for UnreadMessage"""
    pass
