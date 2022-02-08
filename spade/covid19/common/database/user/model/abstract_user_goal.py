from abc import ABC

from common.database.abstract_localized_object import AbstractLocalizedObject
from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible


class AbstractUserGoal(AbstractLocalizedObject, AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing a user goal"""
    pass
