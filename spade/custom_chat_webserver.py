import asyncio
import json
import logging
import os
import ssl
import uuid
from typing import Optional

from autobahn.asyncio.websocket import WebSocketServerFactory
from autobahn.asyncio.websocket import WebSocketServerProtocol

from common.custom_chat.agent.integration import CUSTOM_CHAT_SENDER_NAME, forward_chat_message
from common.custom_chat.chat.message_content_factory import CustomChatMessageContentFactory
from common.custom_chat.chat.message_utils import WebSocketMessageUtils
from common.custom_chat.client_notification_manager import ClientNotificationManager
from common.custom_chat.connected_clients_manager import WebSocketConnectedClientsManager
from common.custom_chat.messages import CustomChatMessage
from common.working_contexts import WorkingContext
from covid19.common.database.connection_manager import AbstractCovid19ConnectionManager
from echo.common.chat_websocket_server import (
    CHAT_WEBSOCKET_SERVER_IP, CHAT_WEBSOCKET_SERVER_PORT, CHAT_WEBSOCKET_SERVER_CERT_PATH,
    CHAT_WEBSOCKET_SERVER_KEY_PATH
)

logger = logging.getLogger(__name__)

WORKING_CONTEXT = os.environ.get("CURRENT_WORKING_CONTEXT", WorkingContext.COVID19.value)
"""The working context in which the GatewayAgent should operate"""

if __name__ == '__main__':
    if WORKING_CONTEXT in WorkingContext.values():  # check for legal working context

        if WORKING_CONTEXT == WorkingContext.COVID19.value:
            from covid19.common.bootstrap_agent_names import CUSTOM_CHAT_GATEWAY_JID
            from covid19.common.database.mongo_db_pryv_hybrid.connection import (
                MongoDBAndPryvHybridConnectionManager, DATABASE_NAME, CONNECTION_URI
            )
            from common.pryv.server_domain import PRYV_SERVER_DOMAIN
            from covid19.customchat.agent.gateway_agent import CustomChatGatewayAgent

            connection_manager: AbstractCovid19ConnectionManager = MongoDBAndPryvHybridConnectionManager(
                DATABASE_NAME, CONNECTION_URI, PRYV_SERVER_DOMAIN
            )

            gateway_agent = CustomChatGatewayAgent(
                jid=CUSTOM_CHAT_GATEWAY_JID,
                password="custom_chat_agent_psw",
                chat_sender_name=CUSTOM_CHAT_SENDER_NAME,
                chat_api_token="Unused",  # Unused
                db_connection_manager=connection_manager
            )

        else:
            gateway_agent = None
            logger.error(f"Working context not recognized!!!")

        future = gateway_agent.start()
        future.result()  # wait for the agent to be online before accepting connections


        class CustomChatServerProtocol(WebSocketServerProtocol):

            def __init__(self):
                super().__init__()

                connection_manager.connect_to_db()
                self._unread_messages_dao = connection_manager.get_unread_message_dao()

                self.current_client_identifier: Optional[str] = None
                self.connection_uuid: str = str(uuid.uuid4())

            @staticmethod
            def _check_json_message_correct(json_message: dict) -> bool:
                """Utility method to check that the received websocket message is semantically correct"""
                return (
                        json_message.get(CustomChatMessage.Fields.SENDER_ID_FIELD.value, None) is not None and
                        json_message.get(CustomChatMessage.Fields.TEXT_FIELD.value, None) is not None and
                        json_message.get(CustomChatMessage.Fields.DATE_FIELD.value, None) is not None and
                        json_message.get(CustomChatMessage.Fields.MESSAGE_ID_FIELD.value, None) is not None
                )

            def onConnect(self, request):
                logger.info(" Client connecting from {0} on port {1}".format(request.origin, request.peer))

            def onOpen(self):
                logger.info(" WebSocket connection open.")

            async def onMessage(self, payload, message_is_binary):

                def _send_back_error_message(error_message: str, ws: WebSocketServerProtocol):
                    """Internal function refactoring error sending"""

                    logger.warning(f" {error_message} .. Not forwarding to agent")
                    message_content = CustomChatMessageContentFactory.create_error_message_content(
                        error_message
                    )
                    prepared_message = WebSocketMessageUtils.preprocess_for_websocket(message_content)
                    ws.sendMessage(prepared_message)

                if self.current_client_identifier is None:
                    # The client should send its identifier, as the first message, after establishing the communication
                    client_identifier: str = payload.decode('utf8')
                    logger.info(f" Received Client ID: `{client_identifier}`")
                    if client_identifier.isalnum():
                        self.current_client_identifier = client_identifier
                        WebSocketConnectedClientsManager.get_instance().add_client(
                            self.current_client_identifier, self.connection_uuid, self
                        )
                        # User logged in, so he/she has read all unread messages
                        ClientNotificationManager.get_instance(self._unread_messages_dao).clear_messages(
                            self.current_client_identifier
                        )
                    else:
                        _send_back_error_message(f"The received identifier is not alphanumeric!", self)

                else:
                    # The client already sent its ID with the first message
                    if message_is_binary:
                        logger.warning(" WS: Binary message received: {0} bytes".format(len(payload)))
                        forward_chat_message(
                            json.dumps(CustomChatMessageContentFactory.create_message_content(f"Binary Data")),
                            gateway_agent
                        )
                    else:
                        txt_msg = payload.decode('utf8')
                        logger.info(" WS: Text message received: {0}".format(txt_msg))
                        try:
                            # Checks if the message is JSON deserializable, exception otherwise
                            deserialized = json.loads(txt_msg)
                            if type(deserialized) != dict:
                                raise TypeError(f"The received message was not a JSON object")

                            if self._check_json_message_correct(deserialized):
                                forward_chat_message(txt_msg, gateway_agent)
                            else:
                                _send_back_error_message(f" This is an incomplete message: `{txt_msg}`", self)
                        except (json.JSONDecodeError, TypeError):
                            _send_back_error_message(f" This is not a valid JSON: `{txt_msg}`", self)

            def onClose(self, was_clean, code, reason):
                logger.info(" WebSocket connection closed: {0}".format(reason))
                WebSocketConnectedClientsManager.get_instance().remove_client(
                    self.current_client_identifier, self.connection_uuid
                )
                logger.info(f" Client with ID {self.current_client_identifier} removed from open connections.")


        # f"ws://{CHAT_WEBSOCKET_SERVER_IP}:{CHAT_WEBSOCKET_SERVER_PORT}"
        factory = WebSocketServerFactory()
        factory.protocol = CustomChatServerProtocol

        protocol_string = "ws"
        ssl_context = None

        # Check if the server should use the secure version or not
        if CHAT_WEBSOCKET_SERVER_CERT_PATH and CHAT_WEBSOCKET_SERVER_KEY_PATH:
            protocol_string = "wss"

            cert_path = CHAT_WEBSOCKET_SERVER_CERT_PATH
            key_path = CHAT_WEBSOCKET_SERVER_KEY_PATH

            logger.info(f" Cert path: {cert_path}")
            logger.info(f" Key path: {key_path}")

            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

            try:
                ssl_context.load_cert_chain(cert_path, key_path)
            except (FileNotFoundError, ssl.SSLError):
                logger.error(" Unable to load SSLContext... defaulting to insecure version...", exc_info=True)
                protocol_string = "ws"
                ssl_context = None

        else:
            logger.info(f" No ssl certificate and key path are set. Defaulting to insecure mode...")

        loop = asyncio.get_event_loop()
        server_coroutine = loop.create_server(
            factory, CHAT_WEBSOCKET_SERVER_IP, CHAT_WEBSOCKET_SERVER_PORT, ssl=ssl_context
        )
        server_future = loop.run_until_complete(server_coroutine)

        try:
            logger.info(f" WebSocket server running on: "
                        f"{protocol_string}://{CHAT_WEBSOCKET_SERVER_IP}:{CHAT_WEBSOCKET_SERVER_PORT}")
            loop.run_forever()
        finally:
            server_future.close()
            loop.close()
            gateway_agent.stop()
            logger.warning(" Custom Chat server quit.")
    else:
        logger.error(f" Currently selected working context `{WORKING_CONTEXT}` is not supported")
