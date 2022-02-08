import logging

from common.chat.platform.types import ChatPlatform
from echo.common.agent.strategies.chat_platform.abstract_echo_handling_strategies import (
    AbstractEchoHandlingStrategies
)
from echo.customchat.agent.strategies.chat_platform.custom_chat_handling_strategies import (
    CustomChatEchoHandlingStrategies
)
from echo.telegram.agent.strategies.chat_platform.telegram_handling_strategies import (
    TelegramEchoHandlingStrategies
)

logger = logging.getLogger(__name__)


class HandlingStrategiesFactory:
    """A class containing factory methods for message handling strategies"""

    @staticmethod
    def strategies_for(platform_type: ChatPlatform) -> AbstractEchoHandlingStrategies:
        """A factory method to create a messaging platform, with provided data"""

        if platform_type == ChatPlatform.TELEGRAM:
            return TelegramEchoHandlingStrategies()
        elif platform_type == ChatPlatform.FACEBOOK_MESSENGER:
            logger.warning(f" Not implemented facebook handling strategies creation")
        elif platform_type == ChatPlatform.CUSTOM_CHAT:
            return CustomChatEchoHandlingStrategies()
        else:
            error_message = f"Unhandled chat platform!! `{platform_type}`"
            raise RuntimeError(error_message)
