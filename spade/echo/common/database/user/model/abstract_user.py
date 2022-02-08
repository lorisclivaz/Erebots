from abc import ABC, abstractmethod
from typing import Optional, List

from common.database.abstract_object_with_id import AbstractObjectWithID
from common.database.json_convertible import AbstractJsonConvertible
from common.database.user.abstract_user import AbstractBasicUser
from echo.common.database.user.model.abstract_chat_message import AbstractChatMessage


class AbstractUser(AbstractBasicUser, AbstractObjectWithID, AbstractJsonConvertible, ABC):
    """An abstract model class representing a user profile"""

    @property
    @abstractmethod
    def telegram_id(self) -> Optional[str]:
        """The user telegram_id"""
        pass

    @telegram_id.setter
    @abstractmethod
    def telegram_id(self, new_value: str):
        """Setter for telegram_id field"""
        pass

    @property
    @abstractmethod
    def custom_chat_id(self) -> Optional[str]:
        """The user custom_chat_id"""
        pass

    @custom_chat_id.setter
    @abstractmethod
    def custom_chat_id(self, new_value: str):
        """Setter for custom_chat_id field"""
        pass

    @property
    @abstractmethod
    def pryv_endpoint(self) -> Optional[str]:
        """The user pryv_endpoint"""
        pass

    @pryv_endpoint.setter
    @abstractmethod
    def pryv_endpoint(self, new_value: str):
        """Setter for pryv_endpoint field"""
        pass

    @property
    @abstractmethod
    def registration_completed(self) -> bool:
        """Whether the user completed the registration process"""
        pass

    @registration_completed.setter
    @abstractmethod
    def registration_completed(self, new_value: bool):
        """Setter for registration_completed field"""
        pass

    @property
    @abstractmethod
    def chat_messages(self) -> List[AbstractChatMessage]:
        """The user chat_messages"""
        pass

    @abstractmethod
    def append_chat_message(self, new_value: AbstractChatMessage):
        """Adds the newly provided chat_message to the user ones"""
        pass

    @abstractmethod
    def replace_chat_message(self, obj_id: str, new_value: AbstractChatMessage):
        """Replaces the message with provided id with the new one"""
        pass

    @abstractmethod
    def delete_chat_message(self, obj_id: str):
        """Deletes the message with provided id"""
        pass

    @property
    @abstractmethod
    def chat_images(self) -> List[AbstractChatMessage]:
        """The user chat_images"""
        pass

    @abstractmethod
    def append_chat_image(self, new_value: AbstractChatMessage):
        """Adds the newly provided chat_image to the user ones"""
        pass
