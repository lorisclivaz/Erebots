from abc import ABC, abstractmethod

from common.database.abstract_dao import AbstractDAO, T


class AbstractMessageDAO(AbstractDAO[T], ABC):
    """A base flag class to implement Data Access Object for Messages"""

    @abstractmethod
    def update(self, object_id: str, new_object: T) -> T:
        """Updates the object with id "object_id" with the provided new object"""
        pass
