import logging
from abc import ABC
from typing import Optional

from common.agent.agents.abstract_user_agent import AbstractMessagingPlatformReceiveMessageState
from common.chat.platform.types import ChatPlatform
from common.custom_chat.message_dao import AbstractMessageDAO
from covid19.common.agent.strategies.chat_platform.abstract_covid19_handling_strategies import (
    AbstractCovid19HandlingStrategies
)
from covid19.common.agent.strategies.chat_platform.handling_strategies_factory import HandlingStrategiesFactory
from covid19.common.database.connection_manager import AbstractCovid19ConnectionManager
from covid19.common.database.user.daos import AbstractUnreadMessageDAO
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class AbstractCovid19ReceiveMessageState(AbstractMessagingPlatformReceiveMessageState, ABC):
    """Abstract Covid19 base class to manage messages coming from users, with some default behaviour"""

    def __init__(self):
        super().__init__()

        # Redefine with specific type
        self.user: Optional[AbstractUser] = None
        self.messaging_platform_handling_strategies: Optional[AbstractCovid19HandlingStrategies] = None

    def create_platform_strategies(self, chat_platform: ChatPlatform) -> AbstractCovid19HandlingStrategies:
        return HandlingStrategiesFactory.strategies_for(chat_platform)

    def retrieve_message_dao(self) -> Optional[AbstractMessageDAO]:
        db_connection_manager: AbstractCovid19ConnectionManager = self.agent.db_connection_manager
        if db_connection_manager is None:
            logger.error(" DB connection manager is null... cannot create MessageDAO")
            return None
        elif self.user is None:
            logger.error(" self.user is None... cannot create MessageDAO")
            return None
        else:
            return db_connection_manager.get_chat_messages_dao(self.user)

    def retrieve_unread_message_dao(self) -> Optional[AbstractUnreadMessageDAO]:
        db_connection_manager: AbstractCovid19ConnectionManager = self.agent.db_connection_manager
        if db_connection_manager is None:
            logger.error(" DB connection manager is null... cannot create UnreadMessageDAO")
            return None
        else:
            return db_connection_manager.get_unread_message_dao()
