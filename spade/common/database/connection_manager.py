from abc import ABC, abstractmethod


class AbstractConnectionManager(ABC):
    """A base class to manage database connections"""

    def __init__(self, database_name: str, database_uri: str):
        self.database_name = database_name
        self.database_uri = database_uri

    @abstractmethod
    def connect_to_db(self, alias: str = "default"):
        """Connects to the database"""
        pass

    @abstractmethod
    def disconnect_from_db(self, alias: str = "default"):
        """Disconnects from the database"""
        pass
