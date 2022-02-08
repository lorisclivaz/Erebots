from enum import Enum
from typing import Mapping

from common.chat.language_enum import Language
from common.chat.localization_enum_mixin import PrettyLocalizationEnumMixin


class DifficultyField(PrettyLocalizationEnumMixin, Enum):
    """The enumeration of values about difficulty experienced by the user"""

    IMPOSSIBLE = 0
    VERY_DIFFICULT = 1
    DIFFICULT = 2
    SLIGHTLY_DIFFICULT = 3
    EASY = 4

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[int, Mapping[Language, str]]:
        return {
            cls.IMPOSSIBLE.value: {
                Language.LANGUAGE_ENGLISH: ':dizzy_face: Impossible',
                Language.LANGUAGE_ITALIAN: ':dizzy_face: Impossibile',
                Language.LANGUAGE_FRENCH: ':dizzy_face: Impossible',
                Language.LANGUAGE_GERMAN: ':dizzy_face: Unmöglich',
            },
            cls.VERY_DIFFICULT.value: {
                Language.LANGUAGE_ENGLISH: ':slightly_frowning_face: Very difficult',
                Language.LANGUAGE_ITALIAN: ':slightly_frowning_face: Molto difficile',
                Language.LANGUAGE_FRENCH: ':slightly_frowning_face: Très difficile',
                Language.LANGUAGE_GERMAN: ':slightly_frowning_face: Sehr schwierig',
            },
            cls.DIFFICULT.value: {
                Language.LANGUAGE_ENGLISH: ':neutral_face: Difficult',
                Language.LANGUAGE_ITALIAN: ':neutral_face: Difficile',
                Language.LANGUAGE_FRENCH: ':neutral_face: Difficile',
                Language.LANGUAGE_GERMAN: ':neutral_face: Schwer',
            },
            cls.SLIGHTLY_DIFFICULT.value: {
                Language.LANGUAGE_ENGLISH: ':slightly_smiling_face: Slightly difficult',
                Language.LANGUAGE_ITALIAN: ':slightly_smiling_face: Un po\' difficile',
                Language.LANGUAGE_FRENCH: ':slightly_smiling_face: Un peu difficile',
                Language.LANGUAGE_GERMAN: ':slightly_smiling_face: Etwas schwierig',
            },
            cls.EASY.value: {
                Language.LANGUAGE_ENGLISH: ':smiling_face_with_sunglasses: Easy',
                Language.LANGUAGE_ITALIAN: ':smiling_face_with_sunglasses: Facile',
                Language.LANGUAGE_FRENCH: ':smiling_face_with_sunglasses: Facile',
                Language.LANGUAGE_GERMAN: ':smiling_face_with_sunglasses: Einfach',
            },
        }


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


class FunnyField(PrettyLocalizationEnumMixin, Enum):
    """The enumeration of values about fun experienced by the user"""

    FUNNY = 'FUNNY'
    INDIFFERENT = 'INDIFFERENT'
    NOT_FUNNY = 'NOT_FUNNY'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.FUNNY.value: {
                Language.LANGUAGE_ENGLISH: ':partying_face: I had fun',
                Language.LANGUAGE_ITALIAN: ':partying_face: Mi sono divertito',
                Language.LANGUAGE_FRENCH: ':partying_face: Je me suis amusé',
                Language.LANGUAGE_GERMAN: ':partying_face: Ich hatte Spaß',
            },
            cls.INDIFFERENT.value: {
                Language.LANGUAGE_ENGLISH: ":expressionless_face: Indifferent",
                Language.LANGUAGE_ITALIAN: ":expressionless_face: Indifferente",
                Language.LANGUAGE_FRENCH: ":expressionless_face: Indifférent",
                Language.LANGUAGE_GERMAN: ":expressionless_face: Gleichgültig",
            },
            cls.NOT_FUNNY.value: {
                Language.LANGUAGE_ENGLISH: ':yawning_face: I didn\'t have fun',
                Language.LANGUAGE_ITALIAN: ':yawning_face: Non mi sono divertito',
                Language.LANGUAGE_FRENCH: ':yawning_face: Je n\'ai pas eu de plaisir',
                Language.LANGUAGE_GERMAN: ':yawning_face: Ich hatte keinen Spaß',
            },
        }
