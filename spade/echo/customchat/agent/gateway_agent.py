import logging

from common.agent.my_logging import log, log_agent_contacts
from common.custom_chat.mixins import CustomChatMixin
from echo.common.agent.agents.abstract_echo_gateway_agent import AbstractEchoGatewayAgent
from echo.common.database.connection_manager import AbstractEchoConnectionManager

logger = logging.getLogger(__name__)


class CustomChatGatewayAgent(AbstractEchoGatewayAgent):
    """The CustomChat Gateway Agent between the chat and the Multi-Agent System for echo project"""

    # In CustomChat version the chat_api_token parameter is unused
    def __init__(self, jid, password, chat_sender_name: str, chat_api_token: str,
                 db_connection_manager: AbstractEchoConnectionManager):
        super().__init__(jid, password, chat_sender_name, chat_api_token, db_connection_manager)

    async def setup(self):
        await super().setup()
        log(self, "CustomChatGatewayAgent started.", logger)
        log_agent_contacts(self, logger)

    class CheckUserRegistrationState(
        CustomChatMixin,
        AbstractEchoGatewayAgent.AbstractCheckUserRegistrationState
    ):
        """The concrete registration checking state using CustomChatMixin"""

        STATE_NAME = "CheckUserRegistrationState"

        def __init__(self, chat_api_token: str):
            # with multiple inheritance all constructors must be called explicitly
            super().__init__(chat_api_token)
            AbstractEchoGatewayAgent.AbstractCheckUserRegistrationState.__init__(self, chat_api_token)

    class HandleUserRegistrationResponseState(
        CustomChatMixin,
        AbstractEchoGatewayAgent.AbstractHandleUserRegistrationResponseState
    ):
        """The concrete response handling state"""

        STATE_NAME = "HandleUserRegistrationResponseState"

        def __init__(self, chat_api_token: str):
            # with multiple inheritance all constructors must be called explicitly
            super().__init__(chat_api_token)
            AbstractEchoGatewayAgent.AbstractHandleUserRegistrationResponseState.__init__(self, chat_api_token)

    def create_check_user_registration_state(self, messaging_platform_api_token: str) -> \
            AbstractEchoGatewayAgent.AbstractCheckUserRegistrationState:
        return CustomChatGatewayAgent.CheckUserRegistrationState(messaging_platform_api_token)

    def create_handle_user_registration_response_state(self, messaging_platform_api_token: str) -> \
            AbstractEchoGatewayAgent.AbstractHandleUserRegistrationResponseState:
        return CustomChatGatewayAgent.HandleUserRegistrationResponseState(messaging_platform_api_token)
