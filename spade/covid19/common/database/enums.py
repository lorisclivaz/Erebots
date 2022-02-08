from enum import Enum
from typing import List, Mapping

from common.chat.language_enum import Language
from common.chat.localization_enum_mixin import PrettyLocalizationEnumMixin
from common.utils.lists import half_values


class AgeField(PrettyLocalizationEnumMixin):
    """The enumeration of values that the "age" field can assume"""

    AGE_18_24 = 'AGE_18_24'
    """Age between 18 and 24 years"""

    AGE_25_34 = 'AGE_25_34'
    """Age between 25 and 34 years"""

    AGE_35_44 = 'AGE_35_44'
    """Age between 35 and 44 years"""

    AGE_45_54 = 'AGE_45_54'
    """Age between 45 and 54 years"""

    AGE_55_64 = 'AGE_55_64'
    """Age between 55 and 64 years"""

    AGE_65_OR_MORE = 'AGE_65_+'
    """Age above 65 years"""

    @staticmethod
    def young() -> List[str]:
        """The first half of the values"""
        return half_values(AgeField.values())

    @staticmethod
    def old() -> List[str]:
        """The second half of the values"""
        return half_values(AgeField.values(), first_half=False)

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        def prettify_not_localized(age_value: str):
            bounds = age_value.split("_")
            return {
                Language.LANGUAGE_ENGLISH:
                    f"Between {bounds[1]} and {bounds[2]}" if bounds[2] != "+" else f"{bounds[1]} or more",
                Language.LANGUAGE_ITALIAN:
                    f"Tra {bounds[1]} e {bounds[2]}" if bounds[2] != "+" else f"{bounds[1]} o più",
                Language.LANGUAGE_FRENCH:
                    f"Entre {bounds[1]} et {bounds[2]}" if bounds[2] != "+" else f"{bounds[1]} ou plus",
                Language.LANGUAGE_GERMAN:
                    f"Zwischen {bounds[1]} und {bounds[2]}" if bounds[2] != "+" else f"{bounds[1]} oder mehr",
            }

        return {value: prettify_not_localized(value) for value in cls.values()}


class SexField(PrettyLocalizationEnumMixin, Enum):
    """The enumeration of values that the "sex" field can assume"""

    SEX_MALE = 'SEX_M'
    """Male"""

    SEX_FEMALE = 'SEX_W'
    """Female"""

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.SEX_MALE.value: {
                Language.LANGUAGE_ENGLISH: ":male_sign: Male",
                Language.LANGUAGE_ITALIAN: ":male_sign: Maschio",
                Language.LANGUAGE_FRENCH: ":male_sign: Mâle",
                Language.LANGUAGE_GERMAN: ":male_sign: Männlich",
            },
            cls.SEX_FEMALE.value: {
                Language.LANGUAGE_ENGLISH: ":female_sign: Female",
                Language.LANGUAGE_ITALIAN: ":female_sign: Femmina",
                Language.LANGUAGE_FRENCH: ":female_sign: Femme",
                Language.LANGUAGE_GERMAN: ":female_sign: Weiblich",
            }
        }


class Usefulness(PrettyLocalizationEnumMixin, Enum):
    """Enumeration with values of usefulness"""

    USEFUL = 'USEFUL'
    INDIFFERENT = 'INDIFFERENT'
    NOT_USEFUL = 'NOT_USEFUL'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.USEFUL.value: {
                Language.LANGUAGE_ENGLISH: ":thumbs_up: Useful",
                Language.LANGUAGE_ITALIAN: ":thumbs_up: Utile",
                Language.LANGUAGE_FRENCH: ":thumbs_up: Utile",
                Language.LANGUAGE_GERMAN: ":thumbs_up: Nützlich",
            },
            cls.INDIFFERENT.value: {
                Language.LANGUAGE_ENGLISH: ":expressionless_face: Indifferent",
                Language.LANGUAGE_ITALIAN: ":expressionless_face: Indifferente",
                Language.LANGUAGE_FRENCH: ":expressionless_face: Indifférent",
                Language.LANGUAGE_GERMAN: ":expressionless_face: Gleichgültig",
            },
            cls.NOT_USEFUL.value: {
                Language.LANGUAGE_ENGLISH: ":thumbs_down: Not Useful",
                Language.LANGUAGE_ITALIAN: ":thumbs_down: Non utile",
                Language.LANGUAGE_FRENCH: ":thumbs_down: Pas utile",
                Language.LANGUAGE_GERMAN: ":thumbs_down: Nicht nützlich",
            },
        }


class WeekDayField(PrettyLocalizationEnumMixin, Enum):
    """The enumeration of values that the "favourite_sport_days" field can assume"""

    MONDAY = 'Monday'
    """Monday"""

    TUESDAY = 'Tuesday'
    """Tuesday"""

    WEDNESDAY = 'Wednesday'
    """Wednesday"""

    THURSDAY = 'Thursday'
    """Thursday"""

    FRIDAY = 'Friday'
    """Friday"""

    SATURDAY = 'Saturday'
    """Saturday"""

    SUNDAY = 'Sunday'
    """Sunday"""

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.MONDAY.value: {
                Language.LANGUAGE_ENGLISH: "Monday",
                Language.LANGUAGE_ITALIAN: "Lunedì",
                Language.LANGUAGE_FRENCH: "Lundi",
                Language.LANGUAGE_GERMAN: "Montag",
            },
            cls.TUESDAY.value: {
                Language.LANGUAGE_ENGLISH: "Tuesday",
                Language.LANGUAGE_ITALIAN: "Martedì",
                Language.LANGUAGE_FRENCH: "Mardi",
                Language.LANGUAGE_GERMAN: "Dienstag",
            },
            cls.WEDNESDAY.value: {
                Language.LANGUAGE_ENGLISH: "Wednesday",
                Language.LANGUAGE_ITALIAN: "Mercoledì",
                Language.LANGUAGE_FRENCH: "Mercredi",
                Language.LANGUAGE_GERMAN: "Mittwoch",
            },
            cls.THURSDAY.value: {
                Language.LANGUAGE_ENGLISH: "Thursday",
                Language.LANGUAGE_ITALIAN: "Giovedì",
                Language.LANGUAGE_FRENCH: "Jeudi",
                Language.LANGUAGE_GERMAN: "Donnerstag",
            },
            cls.FRIDAY.value: {
                Language.LANGUAGE_ENGLISH: "Friday",
                Language.LANGUAGE_ITALIAN: "Venerdì",
                Language.LANGUAGE_FRENCH: "Vendredi",
                Language.LANGUAGE_GERMAN: "Freitag",
            },
            cls.SATURDAY.value: {
                Language.LANGUAGE_ENGLISH: "Saturday",
                Language.LANGUAGE_ITALIAN: "Sabato",
                Language.LANGUAGE_FRENCH: "Samedi",
                Language.LANGUAGE_GERMAN: "Samstag",
            },
            cls.SUNDAY.value: {
                Language.LANGUAGE_ENGLISH: "Sunday",
                Language.LANGUAGE_ITALIAN: "Domenica",
                Language.LANGUAGE_FRENCH: "Dimanche",
                Language.LANGUAGE_GERMAN: "Sonntag",
            },
        }
