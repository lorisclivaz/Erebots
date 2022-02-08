from __future__ import annotations  # Needed in python 3.7 to have the current class type as a return type of methods

import logging
import threading
from typing import Optional, MutableMapping

from autobahn.asyncio import WebSocketServerProtocol

logger = logging.getLogger(__name__)


class WebSocketConnectedClientsManager:
    """A thread-safe singleton class to handle a map of connected clients"""

    __instance = None

    @staticmethod
    def get_instance() -> WebSocketConnectedClientsManager:
        if WebSocketConnectedClientsManager.__instance is None:
            with threading.Lock():  # defensive programming for multiple thread calls to get_instance the first time
                if WebSocketConnectedClientsManager.__instance is None:
                    WebSocketConnectedClientsManager()  # actual creation

        return WebSocketConnectedClientsManager.__instance

    def __init__(self):
        if WebSocketConnectedClientsManager.__instance is not None:
            raise Exception("This is a singleton class, use get_instance method to get the instance")
        else:
            WebSocketConnectedClientsManager.__instance = self

    __client_map: MutableMapping[str, WebSocketServerProtocol] = {}

    MY_UNIQUE_SEPARATOR = ".-.-.-.-.-."

    @staticmethod
    def _compose_client_and_connection_id(client_id: str, connection_id: str) -> str:
        """Method which composes the extended client id, including the connection unique ID"""
        return f"{client_id}{WebSocketConnectedClientsManager.MY_UNIQUE_SEPARATOR}{connection_id}"

    @staticmethod
    def _extract_client_id(extended_client_id: str) -> str:
        """Method to extract client id from its extended version"""
        return extended_client_id.split(WebSocketConnectedClientsManager.MY_UNIQUE_SEPARATOR)[0]

    @staticmethod
    def _log_current_status():
        """Internal method to log current status"""
        connected_ids = [
            WebSocketConnectedClientsManager._extract_client_id(key)
            for key in WebSocketConnectedClientsManager.__client_map.keys()
        ]
        logger.info(f" Currently connected clients: {str(connected_ids)}")

    @staticmethod
    def add_client(client_id: str, connection_unique_id: str, client_ws: WebSocketServerProtocol):
        """Adds a new client connection to websocket mapping. If the client had an open connection this is closed"""
        prev_ws = WebSocketConnectedClientsManager.get_client(client_id)
        if prev_ws is not None:
            logger.info(f" Will close previous connection of `{client_id}`...")
            prev_ws.sendClose(WebSocketServerProtocol.CLOSE_STATUS_CODE_NORMAL)

        extended_client_id = WebSocketConnectedClientsManager._compose_client_and_connection_id(
            client_id, connection_unique_id
        )

        logger.info(f" Adding `{client_id}` connection...")
        WebSocketConnectedClientsManager.__client_map[extended_client_id] = client_ws
        WebSocketConnectedClientsManager._log_current_status()

    @staticmethod
    def remove_client(client_id: str, connection_unique_id: str) -> Optional[WebSocketServerProtocol]:
        """Removes a client ID from websocket mapping, if client ID was present"""
        extended_client_id = WebSocketConnectedClientsManager._compose_client_and_connection_id(
            client_id, connection_unique_id
        )
        logger.info(f" Removing client `{client_id}` ...")
        removed_client = WebSocketConnectedClientsManager.__client_map.pop(extended_client_id, None)
        WebSocketConnectedClientsManager._log_current_status()
        return removed_client

    @staticmethod
    def get_client(client_id: str) -> Optional[WebSocketServerProtocol]:
        """Gets the websocket bound to the provided client ID if present, None otherwise"""
        for extended_client_id, ws in WebSocketConnectedClientsManager.__client_map.items():
            actual_client_id = WebSocketConnectedClientsManager._extract_client_id(extended_client_id)
            if actual_client_id == client_id and ws.is_open:
                return ws

        logger.info(f" No open connection found for `{client_id}`")
        return None
