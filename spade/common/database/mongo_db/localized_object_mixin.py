from abc import ABC
from typing import Optional

from common.database.abstract_localized_object import AbstractLocalizedObject
from common.database.mongo_db import models


class MongoDBLocalizedObjectMixin(AbstractLocalizedObject, ABC):
    """MongoDB Mixin class to automatically implement the AbstractSuggestionMessage specified behaviour"""

    def __init__(self, _mongo_db_obj: models.AbstractLocalizedObject):
        self._localized_object_mongodb_obj: models.AbstractLocalizedObject = _mongo_db_obj

    @property
    def text_en(self) -> str:
        return self._localized_object_mongodb_obj.text_en

    @text_en.setter
    def text_en(self, new_value: str):
        self._localized_object_mongodb_obj.text_en = new_value
        self._localized_object_mongodb_obj.save()

    @property
    def text_it(self) -> Optional[str]:
        return self._localized_object_mongodb_obj.text_it

    @text_it.setter
    def text_it(self, new_value: str):
        self._localized_object_mongodb_obj.text_it = new_value
        self._localized_object_mongodb_obj.save()

    @property
    def text_fr(self) -> Optional[str]:
        return self._localized_object_mongodb_obj.text_fr

    @text_fr.setter
    def text_fr(self, new_value: str):
        self._localized_object_mongodb_obj.text_fr = new_value
        self._localized_object_mongodb_obj.save()

    @property
    def text_de(self) -> Optional[str]:
        return self._localized_object_mongodb_obj.text_de

    @text_de.setter
    def text_de(self, new_value: str):
        self._localized_object_mongodb_obj.text_de = new_value
        self._localized_object_mongodb_obj.save()
