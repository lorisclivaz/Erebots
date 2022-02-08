from abc import ABC, abstractmethod

from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform


class AbstractMessagingPlatformMixin(ABC):
    """A mixin class to introduce the messaging platform property"""

    def __init__(self, messaging_platform_api_token: str):
        self.messaging_platform_api_token = messaging_platform_api_token

    @property
    @abstractmethod
    def messaging_platform(self) -> AbstractMessagingPlatform:
        """A property returning an object representing the messaging platform with its available actions"""
        pass
