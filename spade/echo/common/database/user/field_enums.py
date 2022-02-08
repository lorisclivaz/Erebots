from enum import Enum
from typing import Mapping

from common.chat.language_enum import Language
from common.chat.localization_enum_mixin import PrettyLocalizationEnumMixin


class ShiftField(PrettyLocalizationEnumMixin, Enum):
    """The enumeration of values that expresses shifting to the next or previous element"""

    PREVIOUS = 'PREVIOUS'
    NEXT = 'NEXT'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.PREVIOUS.value: {
                Language.LANGUAGE_ENGLISH: ':left_arrow:',
                Language.LANGUAGE_ITALIAN: ':left_arrow:',
                Language.LANGUAGE_FRENCH: ':left_arrow:',
                Language.LANGUAGE_GERMAN: ':left_arrow:',
            },
            cls.NEXT.value: {
                Language.LANGUAGE_ENGLISH: ':right_arrow:',
                Language.LANGUAGE_ITALIAN: ':right_arrow:',
                Language.LANGUAGE_FRENCH: ':right_arrow:',
                Language.LANGUAGE_GERMAN: ':right_arrow:',
            },
        }
