from typing import Optional, List

from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from common.database.mongo_db.user.user_mixin import MongoDBUserMixin
from echo.common.database.mongo_db.models import User
from echo.common.database.user.model.abstract_chat_message import AbstractChatMessage
from echo.common.database.user.model.abstract_user import AbstractUser


class MongoDBUser(AbstractUser, MongoDBUserMixin, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractUser for MongoDB"""

    def __init__(self, _mongo_db_obj: User):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        MongoDBUserMixin.__init__(self, _mongo_db_obj)
        self._user_mongodb_obj: User = _mongo_db_obj

    @property
    def telegram_id(self) -> Optional[str]:
        return self._user_mongodb_obj.telegram_id

    @telegram_id.setter
    def telegram_id(self, new_value: str):
        self._user_mongodb_obj.telegram_id = new_value
        self._user_mongodb_obj.save()

    @property
    def custom_chat_id(self) -> Optional[str]:
        return self._user_mongodb_obj.custom_chat_id

    @custom_chat_id.setter
    def custom_chat_id(self, new_value: str):
        self._user_mongodb_obj.custom_chat_id = new_value
        self._user_mongodb_obj.save()

    @property
    def pryv_endpoint(self) -> Optional[str]:
        return self._user_mongodb_obj.pryv_endpoint

    @pryv_endpoint.setter
    def pryv_endpoint(self, new_value: str):
        self._user_mongodb_obj.pryv_endpoint = new_value
        self._user_mongodb_obj.save()

    @property
    def registration_completed(self) -> bool:
        return self._user_mongodb_obj.registration_completed

    @registration_completed.setter
    def registration_completed(self, new_value: bool):
        self._user_mongodb_obj.registration_completed = new_value
        self._user_mongodb_obj.save()

    @property
    def chat_messages(self) -> List[AbstractChatMessage]:
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def append_chat_message(self, new_value: AbstractChatMessage):
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def replace_chat_message(self, obj_id: str, new_value: AbstractChatMessage):
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def delete_chat_message(self, obj_id: str):
        raise NotImplementedError("Not implemented since we were using pryv for this")

    @property
    def chat_images(self) -> List[AbstractChatMessage]:
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def append_chat_image(self, new_value: AbstractChatMessage):
        raise NotImplementedError("Not implemented since we were using pryv for this")

    def to_json_string(self) -> str:
        return self._user_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, user_json: str):
        """Creates a MongoDBUser from a json string"""

        return cls(User.from_json(user_json))
