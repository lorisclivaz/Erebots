from enum import Enum
from typing import TypeVar, List

EnumValueType = TypeVar('EnumValueType')


class ValuesMixin(Enum):
    """A mixin adding the "values" getter to enumerations"""

    @classmethod
    def values(cls) -> List[EnumValueType]: return [element.value for element in cls]
