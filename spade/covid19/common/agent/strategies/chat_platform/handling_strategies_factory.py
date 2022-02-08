import logging

from common.chat.platform.types import ChatPlatform
from covid19.common.agent.strategies.chat_platform.abstract_covid19_handling_strategies import (
    AbstractCovid19HandlingStrategies
)
from covid19.customchat.agent.strategies.chat_platform.custom_chat_handling_strategies import (
    CustomChatCovid19HandlingStrategies
)
from covid19.telegram.agent.strategies.chat_platform.telegram_handling_strategies import (
    TelegramCovid19HandlingStrategies
)

logger = logging.getLogger(__name__)


class HandlingStrategiesFactory:
    """A class containing factory methods for message handling strategies"""

    @staticmethod
    def strategies_for(platform_type: ChatPlatform) -> AbstractCovid19HandlingStrategies:
        """A factory method to create a messaging platform, with provided data"""

        if platform_type == ChatPlatform.TELEGRAM:
            return TelegramCovid19HandlingStrategies()
        elif platform_type == ChatPlatform.FACEBOOK_MESSENGER:
            logger.warning(f" Not implemented facebook handling strategies creation")
        elif platform_type == ChatPlatform.CUSTOM_CHAT:
            return CustomChatCovid19HandlingStrategies()
        else:
            error_message = f"Unhandled chat platform!! `{platform_type}`"
            raise RuntimeError(error_message)
