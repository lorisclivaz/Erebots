from __future__ import annotations  # Needed in python 3.7 to have the current class type as a return type of methods

import logging
import threading
from typing import Optional, List

from echo.common.database.user.daos import AbstractUnreadMessageDAO
from echo.common.database.user.factory import UnreadMessageFactory
from echo.common.database.user.model.abstract_unread_message import AbstractUnreadMessage

logger = logging.getLogger(__name__)


class ClientNotificationManager:
    """A thread-safe singleton class to handle client not sent messages"""

    __instance: ClientNotificationManager = None

    @staticmethod
    def get_instance(unread_message_dao: AbstractUnreadMessageDAO) -> ClientNotificationManager:
        if ClientNotificationManager.__instance is None:
            with threading.Lock():  # defensive programming for multiple thread calls to get_instance the first time
                if ClientNotificationManager.__instance is None:
                    ClientNotificationManager(unread_message_dao)  # actual creation

        return ClientNotificationManager.__instance

    def __init__(self, unread_message_dao: AbstractUnreadMessageDAO):
        if ClientNotificationManager.__instance is not None:
            raise Exception("This is a singleton class, use get_instance method to get the instance")
        else:
            self.unread_message_dao = unread_message_dao
            ClientNotificationManager.__instance = self

    def get_messages(self, for_client_id: str) -> Optional[List[dict]]:
        """Gets the client's unread messages if present, empty list otherwise"""
        client_unread_messages: List[AbstractUnreadMessage] = list(
            self.unread_message_dao.find_by(recipient_id=for_client_id).values()
        )
        self.clear_messages(for_client_id)
        return [message.message_json for message in client_unread_messages]

    def add_message(self, to_client_id: str, message_obj: dict):
        """Adds a new client unread message"""
        self.unread_message_dao.insert(
            UnreadMessageFactory.new_unread_message(to_client_id, message_obj)
        )

        logger.info(f" Saved unread message for `{to_client_id}`: {str(message_obj)}")

    def clear_messages(self, for_client_id: str):
        """Clears unread messages for a client ID"""

        unread_messages = self.unread_message_dao.find_by(recipient_id=for_client_id).values()

        if len(unread_messages) == 0:
            logger.info(f" No unread messages to clear.")

        for unread_message in unread_messages:
            self.unread_message_dao.delete_by_id(unread_message.id)
