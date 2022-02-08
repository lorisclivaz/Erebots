import logging
from typing import Optional

from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform
from common.chat.platform.types import ChatPlatform
from common.custom_chat.chat.messaging_platform import CustomChatMessagingPlatform
from common.custom_chat.client_notification_manager import ClientNotificationManager
from common.custom_chat.connected_clients_manager import WebSocketConnectedClientsManager
from common.custom_chat.message_dao import AbstractMessageDAO
from common.telegram.chat.messaging_platform import TelegramMessagingPlatform
from echo.common.database.user.daos import AbstractUnreadMessageDAO

logger = logging.getLogger(__name__)


class MessagingPlatformFactory:
    """A class containing factory methods for messaging platforms"""

    @staticmethod
    def platform_from(platform_type: ChatPlatform, messaging_platform_api_token: str,
                      message_dao: Optional[AbstractMessageDAO] = None,
                      unread_message_dao: Optional[AbstractUnreadMessageDAO] = None) -> AbstractMessagingPlatform:
        """A factory method to create a messaging platform, with provided data"""

        if platform_type == ChatPlatform.TELEGRAM:
            return TelegramMessagingPlatform(messaging_platform_api_token)
        elif platform_type == ChatPlatform.FACEBOOK_MESSENGER:
            logger.warning(f" Not implemented facebook messaging platform creation")
        elif platform_type == ChatPlatform.CUSTOM_CHAT:
            return CustomChatMessagingPlatform(
                messaging_platform_api_token,
                WebSocketConnectedClientsManager.get_instance(),
                message_dao,
                ClientNotificationManager.get_instance(unread_message_dao) if unread_message_dao else None
            )
