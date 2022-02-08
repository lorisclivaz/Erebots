from abc import abstractmethod
from typing import Mapping, List, Optional

from common.chat.language_enum import Language
from common.utils.enums import ValuesMixin, EnumValueType


# TODO 04/06/2020: this could be used to localize Profiles bot
class PrettyLocalizationEnumMixin(ValuesMixin):
    """A base class to inject pretty localization capabilities in enumerations"""

    @staticmethod
    def default_language() -> Language:
        return Language.LANGUAGE_ENGLISH

    @classmethod
    @abstractmethod
    def values_prettifier_not_localized(cls) -> Mapping[EnumValueType, Mapping[Language, str]]:
        """Returns a dictionary containing a mapping between each value and its pretty version, not localized"""
        pass

    @classmethod
    def pretty_values_not_localized(cls) -> List[Mapping[Language, str]]:
        """List of pretty-values localization-mappings"""

        ugly_to_pretty_localization_mappings = cls.values_prettifier_not_localized()
        return [ugly_to_pretty_localization_mappings[ugly_value] for ugly_value in cls.values()]

    @classmethod
    def values_prettifier_localized(cls, language: Optional[Language]) -> Mapping[EnumValueType, str]:
        """Returns a dictionary containing a mapping between each value and its pretty version, localized"""

        return {
            value: localizer.get(language, localizer[cls.default_language()])
            for value, localizer in cls.values_prettifier_not_localized().items()
        }

    @classmethod
    def pretty_values_localized(cls, language: Optional[Language]) -> List[str]:
        """List of values, prettified and localized"""

        return [localizer.get(language, localizer[cls.default_language()])
                for localizer in cls.pretty_values_not_localized()]

    @classmethod
    def uglify(cls, pretty_localized_value: str) -> Optional[EnumValueType]:
        """
        Utility method to revert back the prettifying effect, and get the raw Enum value,
        or None if no match found
        """

        for ugly_value, localization_pretty_mappings in cls.values_prettifier_not_localized().items():
            for _, pretty_value in localization_pretty_mappings.items():
                if pretty_value == pretty_localized_value:
                    return ugly_value

        return None
