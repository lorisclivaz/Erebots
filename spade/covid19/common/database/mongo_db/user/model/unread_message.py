import json

from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from covid19.common.database.mongo_db.models import (
    UnreadMessage
)
from covid19.common.database.user.model.abstract_unread_message import (
    AbstractUnreadMessage
)


class MongoDBUnreadMessage(AbstractUnreadMessage, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractUnreadMessage for MongoDB"""

    def __init__(self, _mongo_db_obj: UnreadMessage):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        self._unread_message_mongodb_obj: UnreadMessage = _mongo_db_obj

    @property
    def recipient_id(self) -> str:
        return self._unread_message_mongodb_obj.recipient_id

    @recipient_id.setter
    def recipient_id(self, new_value: str):
        self._unread_message_mongodb_obj.recipient_id = new_value
        self._unread_message_mongodb_obj.save()

    @property
    def message_json(self) -> dict:
        return json.loads(self._unread_message_mongodb_obj.message_json)

    @message_json.setter
    def message_json(self, new_value: dict):
        self._unread_message_mongodb_obj.message_json = json.dumps(new_value)
        self._unread_message_mongodb_obj.save()

    def to_json_string(self) -> str:
        return self._unread_message_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, unread_message_json: str):
        """Creates a MongoDBUnreadMessage from a json string"""

        return cls(UnreadMessage.from_json(unread_message_json))
