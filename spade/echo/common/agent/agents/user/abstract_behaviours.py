import logging
from abc import ABC
from typing import Optional

from common.agent.agents.abstract_user_agent import AbstractMessagingPlatformReceiveMessageState
from common.chat.platform.types import ChatPlatform
from common.custom_chat.message_dao import AbstractMessageDAO
from echo.common.agent.strategies.chat_platform.abstract_echo_handling_strategies import (
    AbstractEchoHandlingStrategies
)
from echo.common.agent.strategies.chat_platform.handling_strategies_factory import HandlingStrategiesFactory
from echo.common.database.connection_manager import AbstractEchoConnectionManager
from echo.common.database.user.daos import AbstractUnreadMessageDAO
from echo.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class AbstractEchoReceiveMessageState(AbstractMessagingPlatformReceiveMessageState, ABC):
    """Abstract echo base class to manage messages coming from users, with some default behaviour"""

    def __init__(self):
        super().__init__()

        # Redefine with specific type
        self.user: Optional[AbstractUser] = None
        self.messaging_platform_handling_strategies: Optional[AbstractEchoHandlingStrategies] = None
        self.platform_type: Optional[ChatPlatform] = None

    def create_platform_strategies(self, chat_platform: ChatPlatform) -> AbstractEchoHandlingStrategies:
        self.platform_type = chat_platform
        return HandlingStrategiesFactory.strategies_for(chat_platform)

    def retrieve_message_dao(self) -> Optional[AbstractMessageDAO]:
        db_connection_manager: AbstractEchoConnectionManager = self.agent.db_connection_manager
        if db_connection_manager is None:
            logger.error(" DB connection manager is null... cannot create MessageDAO")
            return None
        elif self.user is None:
            logger.error(" self.user is None... cannot create MessageDAO")
            return None
        else:
            return db_connection_manager.get_chat_messages_dao(self.user)

    def retrieve_unread_message_dao(self) -> Optional[AbstractUnreadMessageDAO]:
        db_connection_manager: AbstractEchoConnectionManager = self.agent.db_connection_manager
        if db_connection_manager is None:
            logger.error(" DB connection manager is null... cannot create UnreadMessageDAO")
            return None
        else:
            return db_connection_manager.get_unread_message_dao()
