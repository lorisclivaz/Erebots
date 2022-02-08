from abc import ABC, abstractmethod


class AbstractObjectWithID(ABC):
    """A base class to represent all objects with an ID"""

    @property
    @abstractmethod
    def id(self) -> str:
        """The object id"""
        pass
