from __future__ import annotations  # Needed in python 3.7 to have the current class type as a return type of methods

import logging
from enum import Enum
from typing import Mapping, List, Optional, MutableMapping

from common.utils.dictionaries import inverse_dictionary
from common.utils.enums import ValuesMixin

logger = logging.getLogger(__name__)


class Language(ValuesMixin, Enum):
    """The enumeration of values that the "language" field can assume"""

    LANGUAGE_ENGLISH = 'LANGUAGE_ENGLISH'
    """English language"""

    LANGUAGE_ITALIAN = 'LANGUAGE_ITALIAN'
    """Italian language"""

    LANGUAGE_FRENCH = 'LANGUAGE_FRENCH'
    """French language"""

    LANGUAGE_GERMAN = 'LANGUAGE_GERMAN'
    """German language"""

    @staticmethod
    def values_prettifier_dictionary() -> Mapping[str, str]:
        """Returns a dictionary containing a mapping between each values and its pretty version"""
        return {
            'LANGUAGE_ENGLISH': ":United_States: :United_Kingdom: English",
            'LANGUAGE_ITALIAN': ":Italy: Italian",
            'LANGUAGE_FRENCH': ":France: French",
            'LANGUAGE_GERMAN': ":Germany: German",
        }

    @staticmethod
    def pretty_values() -> List[str]:
        """List of values, prettified"""

        ugly_to_pretty = Language.values_prettifier_dictionary()
        return [ugly_to_pretty[ugly_value] for ugly_value in Language.values()]

    @staticmethod
    def _custom_to_ietf_mapping() -> MutableMapping[Language, str]:
        return {
            Language.LANGUAGE_ENGLISH: "en",
            Language.LANGUAGE_ITALIAN: "it",
            Language.LANGUAGE_FRENCH: "fr",
            Language.LANGUAGE_GERMAN: "de",
        }

    @staticmethod
    def from_ietf_tag(language: Optional[str]) -> Optional[Language]:
        """Returns the Language instance from the IETF language tag"""

        if language is None:
            return None
        else:
            inverted_mapping = inverse_dictionary(Language._custom_to_ietf_mapping())
            custom_language = inverted_mapping.get(language, None)
            if custom_language is None:
                logger.warning(f" Language mapping for `{language}` not found!")

            return custom_language

    @staticmethod
    def to_ietf_tag(language: Optional[Language]) -> Optional[str]:
        """Returns the language code of provided language instance"""

        if language is None:
            return None
        else:
            ietf_language = Language._custom_to_ietf_mapping().get(language, None)
            if ietf_language is None:
                logger.warning(f" Language mapping for `{language}` not found!")

            return ietf_language
