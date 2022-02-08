from abc import ABC, abstractmethod
from typing import Optional, Mapping

from common.chat.language_enum import Language
from common.database.json_convertible import AbstractJsonConvertible


class AbstractLocalizedObject(AbstractJsonConvertible, ABC):
    """An abstract base class for all suggestion messages sent to the user"""

    @property
    @abstractmethod
    def text_en(self) -> str:
        """The message text in English"""
        pass

    @text_en.setter
    @abstractmethod
    def text_en(self, new_value: str):
        """Setter for text_en field"""
        pass

    @property
    @abstractmethod
    def text_it(self) -> Optional[str]:
        """The message text in Italian"""
        pass

    @text_it.setter
    @abstractmethod
    def text_it(self, new_value: str):
        """Setter for text_it field"""
        pass

    @property
    @abstractmethod
    def text_fr(self) -> Optional[str]:
        """The message text in French"""
        pass

    @text_fr.setter
    @abstractmethod
    def text_fr(self, new_value: str):
        """Setter for text_fr field"""
        pass

    @property
    @abstractmethod
    def text_de(self) -> Optional[str]:
        """The message text in German"""
        pass

    @text_de.setter
    @abstractmethod
    def text_de(self, new_value: str):
        """Setter for text_de field"""
        pass

    @property
    def text_not_localized(self) -> Mapping[Language, str]:
        """A getter for the the text localization mappings"""

        result_mapping = {Language.LANGUAGE_ENGLISH: self.text_en}

        if self.text_it:
            result_mapping[Language.LANGUAGE_ITALIAN] = self.text_it
        if self.text_fr:
            result_mapping[Language.LANGUAGE_FRENCH] = self.text_fr
        if self.text_de:
            result_mapping[Language.LANGUAGE_GERMAN] = self.text_de

        return result_mapping
