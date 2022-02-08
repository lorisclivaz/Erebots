from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from common.chat.language_enum import Language
from common.database.json_convertible import AbstractJsonConvertible


# TODO 04/06/2020: use this class to refactor Profiles user modelling
class AbstractBasicUser(AbstractJsonConvertible, ABC):
    """Common class to represent a user interacting with the platform"""

    @property
    @abstractmethod
    def first_name(self) -> Optional[str]:
        """The user first_name"""
        pass

    @first_name.setter
    @abstractmethod
    def first_name(self, new_value: str):
        """Setter for first_name field"""
        pass

    @property
    @abstractmethod
    def last_name(self) -> Optional[str]:
        """The user last_name"""
        pass

    @last_name.setter
    @abstractmethod
    def last_name(self, new_value: str):
        """Setter for last_name field"""
        pass

    @property
    @abstractmethod
    def language(self) -> Optional[Language]:
        """The user language"""
        pass

    @language.setter
    @abstractmethod
    def language(self, new_value: Language):
        """Setter for language field"""
        pass

    @property
    @abstractmethod
    def last_interaction(self) -> Optional[datetime]:
        """The user last_interaction"""
        pass

    @last_interaction.setter
    @abstractmethod
    def last_interaction(self, new_value: datetime):
        """Setter for last_interaction field"""
        pass
