from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform
from common.chat.platform.factory import MessagingPlatformFactory
from common.chat.platform.mixins import AbstractMessagingPlatformMixin
from common.chat.platform.types import ChatPlatform


class TelegramMixin(AbstractMessagingPlatformMixin):
    """A mixin to get access to a TelegramBot instance"""

    def __init__(self, telegram_api_token: str):
        super().__init__(telegram_api_token)

    @property
    def messaging_platform(self) -> AbstractMessagingPlatform:
        return MessagingPlatformFactory.platform_from(
            ChatPlatform.TELEGRAM, self.messaging_platform_api_token
        )
