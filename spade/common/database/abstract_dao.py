from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Mapping

T = TypeVar('T')


class AbstractDAO(Generic[T], ABC):
    """A base class defining an abstract Data Access Object"""

    @abstractmethod
    def find_by_id(self, object_id: str) -> Optional[T]:
        """Finds an object by ID"""
        pass

    @abstractmethod
    def find_by(self, **kwargs) -> Mapping[str, T]:
        """Finds all objects matching the given filters, returning a mapping between id and the object"""
        pass

    @abstractmethod
    def count(self) -> int:
        """Returns the count of saved objects"""
        pass

    @abstractmethod
    def insert(self, new_object: T) -> T:
        """Inserts provided new object in DB, and returns its database bound instance (filled with ID)"""
        pass

    @abstractmethod
    def delete_by_id(self, object_id: str) -> bool:
        """Deletes an object by ID, returning True on success"""
        pass
