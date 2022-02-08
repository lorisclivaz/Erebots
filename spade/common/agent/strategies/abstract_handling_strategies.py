from abc import abstractmethod, ABC
from typing import Collection, Any, Optional, Dict

from common.chat.message.types import ChatMessage
from common.database.user.abstract_user import AbstractBasicUser


class AbstractHandlingStrategies(ABC):
    """A base class for handling strategies to manage messages received in UserAgent"""

    @abstractmethod
    def bind_messaging_platform_id_to_user_id(self, user: AbstractBasicUser, chat_message: ChatMessage):
        """
        A method called when a binding between the user platform id and the user id could be established

        It should have effect only once (this method should be idempotent)
        """
        pass

    @abstractmethod
    def extract_platform_id(self, user: AbstractBasicUser) -> Optional[str]:
        """
        A method to extract the chat platform specific ID from user profile;
        None if the user hasn't that platform ID
        """
        pass

    @abstractmethod
    def create_menu_keyboard_from(self, option_list: Collection[str], row_width: int = None) -> Any:
        """
        A method to create a keyboard with provided option list

        Should return the object to be used as keyboard, or an object to remove custom keyboard if no options provided
        """
        pass

    @abstractmethod
    def create_quick_menu_from(self, option_list: Collection[str]) -> Any:
        """
        A method to create a quick options menu, with provided options

        Should return the menu object
        """
        pass

    @abstractmethod
    def create_inline_menu_from(self, option_dict: Dict[str, str], row_width: int = 3) -> Any:
        """
        A method to create an inline options menu, with provided Dict[button_text, payload] where payload can be either
        an option word or an URL string.

        Should return the menu object
        """
        pass

    @abstractmethod
    def create_show_normal_keyboard(self):
        """
        A method to create a keyboard object that when sent to the user hides the previous custom keyboard
        and shows up the normal message keyboard

        Should return the object that will implement this behaviour on the messaging platform
        """
