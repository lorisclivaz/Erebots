from typing import Mapping, Optional

from common.custom_chat.message_dao import AbstractMessageDAO
from echo.common.database.user.factory import CustomChatMessageFactory
from echo.common.database.user.model.abstract_chat_message import AbstractChatMessage
from echo.common.database.user.model.abstract_user import AbstractUser


class PryvChatMessageDAO(AbstractMessageDAO[AbstractChatMessage]):
    """Actual implementation for Pryv of ChatMessages Access Object"""

    def __init__(self, user: AbstractUser):
        self._user = user

    def find_by_id(self, object_id: str) -> Optional[AbstractChatMessage]:
        user_messages = self._user.chat_messages
        for user_message in user_messages:
            if user_message.message_id == object_id:
                return user_message

    def find_by(self, **kwargs) -> Mapping[str, AbstractChatMessage]:
        raise Exception("Unsupported operation.")

    def count(self) -> int:
        return len(self._user.chat_messages)

    def insert(self, new_object: dict) -> AbstractChatMessage:
        new_message = CustomChatMessageFactory.new_chat_message(new_object)
        if new_message.payload.get('photo') is None:
            self._user.append_chat_message(new_message)
        else:
            self._user.append_chat_image(new_message)
        return new_message

    def update(self, object_id: str, new_object: dict) -> AbstractChatMessage:
        new_message = CustomChatMessageFactory.new_chat_message(new_object)
        self._user.replace_chat_message(object_id, new_message)
        return new_message

    def delete_by_id(self, object_id: str) -> bool:
        try:
            self._user.delete_chat_message(object_id)
            return True
        except:
            return False
