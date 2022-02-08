from dataclasses import dataclass

from bson import json_util

from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from echo.common.database.user.model.abstract_unread_message import AbstractUnreadMessage


@dataclass
class UnreadMessageBean(AbstractUnreadMessage, ObjectWithIDBeanMixin):
    """A bean class to create unread messages, not directly bound to a database instance"""

    recipient_id: str
    message_json: dict

    def recipient_id(self) -> str:
        return self.recipient_id

    def message_json(self) -> dict:
        return json_util.loads(self.message_json)

    def to_json_string(self) -> str:
        return json_util.dumps({
            'recipient_id': self.recipient_id,
            'message_json': json_util.dumps(self.message_json),
        })
