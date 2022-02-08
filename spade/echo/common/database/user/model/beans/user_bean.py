import json
from dataclasses import dataclass
from typing import Optional, List

from bson import json_util

from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from common.database.user.beans.user_bean_mixin import BasicUserBeanMixin
from echo.common.database.user.model.abstract_chat_message import AbstractChatMessage
from echo.common.database.user.model.abstract_user import AbstractUser


@dataclass
class UserBean(AbstractUser, BasicUserBeanMixin, ObjectWithIDBeanMixin):
    """A bean class to create users not directly bound to a database instance"""

    telegram_id: Optional[str] = None
    custom_chat_id: Optional[str] = None
    pryv_endpoint: Optional[str] = None
    registration_completed: bool = False
    chat_messages: Optional[List[AbstractChatMessage]] = None

    def append_chat_message(self, new_value: AbstractChatMessage):
        self.chat_messages.append(new_value)

    def replace_chat_message(self, obj_id: str, new_value: AbstractChatMessage):
        self.chat_messages = [obj if obj.message_id != obj_id else new_value
                              for obj in self.chat_messages]

    def delete_chat_message(self, obj_id: str):
        self.chat_messages = [obj for obj in self.chat_messages
                              if obj.message_id != obj_id]

    def to_json_string(self) -> str:
        return json_util.dumps({
            **json.loads(BasicUserBeanMixin.to_json_string(self)),
            'telegram_id': self.telegram_id,
            'custom_chat_id': self.custom_chat_id,
            'pryv_endpoint': self.pryv_endpoint,
            'registration_completed': self.registration_completed,
            'chat_messages': [
                chat_message.to_json() for chat_message in self.chat_messages
            ] if self.chat_messages else [],
        })
