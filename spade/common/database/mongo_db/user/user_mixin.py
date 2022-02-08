from abc import ABC
from datetime import datetime
from typing import Optional

from common.chat.language_enum import Language
from common.database.mongo_db.models import BasicUser
from common.database.user.abstract_user import AbstractBasicUser


class MongoDBUserMixin(AbstractBasicUser, ABC):
    """MongoDB Mixin class to automatically implement the AbstractUser specified behaviour"""

    def __init__(self, _mongo_db_obj: BasicUser):
        self._user_mongodb_obj: BasicUser = _mongo_db_obj

    @property
    def first_name(self) -> Optional[str]:
        return self._user_mongodb_obj.first_name

    @first_name.setter
    def first_name(self, new_value: str):
        self._user_mongodb_obj.first_name = new_value
        self._user_mongodb_obj.save()

    @property
    def last_name(self) -> Optional[str]:
        return self._user_mongodb_obj.last_name

    @last_name.setter
    def last_name(self, new_value: str):
        self._user_mongodb_obj.last_name = new_value
        self._user_mongodb_obj.save()

    @property
    def language(self) -> Optional[Language]:
        language = self._user_mongodb_obj.language
        return Language(language) if language else None

    @language.setter
    def language(self, new_value: Language):
        self._user_mongodb_obj.language = new_value.value
        self._user_mongodb_obj.save()

    @property
    def last_interaction(self) -> Optional[datetime]:
        return self._user_mongodb_obj.last_interaction

    @last_interaction.setter
    def last_interaction(self, new_value: datetime):
        self._user_mongodb_obj.last_interaction = new_value
        self._user_mongodb_obj.save()
