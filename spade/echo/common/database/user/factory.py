from datetime import datetime
from typing import Optional

from common.chat.language_enum import Language
from echo.common.database.mongo_db.user.model.unread_message import MongoDBUnreadMessage
from echo.common.database.mongo_db.user.model.user import MongoDBUser
from echo.common.database.user.model.abstract_chat_message import AbstractChatMessage
from echo.common.database.user.model.abstract_unread_message import AbstractUnreadMessage
from echo.common.database.user.model.abstract_user import AbstractUser
from echo.common.database.user.model.beans.chat_message_bean import ChatMessageBean
from echo.common.database.user.model.beans.unread_message_bean import UnreadMessageBean
from echo.common.database.user.model.beans.user_bean import UserBean


class CustomChatMessageFactory:
    """A class containing factory methods for ChatMessage"""

    @staticmethod
    def new_chat_message(payload: dict, ) -> AbstractChatMessage:
        """A factory method to create a new ChatMessage"""

        return ChatMessageBean(payload=payload)


class UnreadMessageFactory:
    """A class containing factory method for UnreadMessage"""

    @staticmethod
    def new_unread_message(recipient_id: str, message_json: dict) -> AbstractUnreadMessage:
        """A factory method to create a new UnreadMessage"""

        return UnreadMessageBean(recipient_id, message_json)

    @staticmethod
    def from_json(unread_message_json: str) -> AbstractUnreadMessage:
        """A factory method to create an UnreadMessage from a JSON string"""

        return MongoDBUnreadMessage.from_json(unread_message_json)


class UserFactory:
    """A class containing factory methods for Users"""

    @staticmethod
    def new_user(
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            language: Optional[Language] = None,
            last_interaction: datetime = datetime.min,
            telegram_id: Optional[str] = None,
            custom_chat_id: Optional[str] = None,
            pryv_endpoint: Optional[str] = None,
            registration_completed: bool = False,
    ) -> AbstractUser:
        """A factory method to create a new User"""

        return UserBean(first_name, last_name, language, last_interaction, telegram_id, custom_chat_id, pryv_endpoint,
                        registration_completed)

    @staticmethod
    def from_json(user_json: str) -> AbstractUser:
        """A factory method to create a User from a JSON string"""

        return MongoDBUser.from_json(user_json)
