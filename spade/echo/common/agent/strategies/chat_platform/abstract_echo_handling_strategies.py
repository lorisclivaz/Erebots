from abc import ABC, abstractmethod
from typing import Any, Optional

from common.agent.strategies.abstract_handling_strategies import AbstractHandlingStrategies
from common.chat.language_enum import Language


class AbstractEchoHandlingStrategies(AbstractHandlingStrategies, ABC):
    """A base class for handling strategies for message receiving in UserAgent"""

    @abstractmethod
    def create_main_menu_keyboard(self, language: Optional[Language]) -> Any:
        """
        A method to create the main reply keyboard, localized

        Should return the object to be used as keyboard
        """
        pass
