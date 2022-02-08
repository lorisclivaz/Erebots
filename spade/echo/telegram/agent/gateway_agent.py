import logging

from common.agent.my_logging import log, log_agent_contacts
from common.telegram.mixins import TelegramMixin
from echo.common.agent.agents.abstract_echo_gateway_agent import AbstractEchoGatewayAgent
from echo.common.database.connection_manager import AbstractEchoConnectionManager

logger = logging.getLogger(__name__)


class TelegramGatewayAgent(AbstractEchoGatewayAgent):
    """The Telegram Gateway Agent between Telegram and the Multi-Agent System for echo project"""

    def __init__(self, jid, password, telegram_sender_name: str, telegram_api_token: str,
                 db_connection_manager: AbstractEchoConnectionManager):
        super().__init__(jid, password, telegram_sender_name, telegram_api_token, db_connection_manager)

    async def setup(self):
        await super().setup()
        log(self, "TelegramGatewayAgent started.", logger)
        log_agent_contacts(self, logger)

    class CheckUserRegistrationState(
        TelegramMixin,
        AbstractEchoGatewayAgent.AbstractCheckUserRegistrationState
    ):
        """The concrete registration checking state using TelegramMixin"""

        STATE_NAME = "CheckUserRegistrationState"

        def __init__(self, telegram_api_token: str):
            # with multiple inheritance all constructors must be called explicitly
            super().__init__(telegram_api_token)
            AbstractEchoGatewayAgent.AbstractCheckUserRegistrationState.__init__(self, telegram_api_token)

    class HandleUserRegistrationResponseState(
        TelegramMixin,
        AbstractEchoGatewayAgent.AbstractHandleUserRegistrationResponseState
    ):
        """The concrete response handling state"""

        STATE_NAME = "HandleUserRegistrationResponseState"

        def __init__(self, telegram_api_token: str):
            # with multiple inheritance all constructors must be called explicitly
            super().__init__(telegram_api_token)
            AbstractEchoGatewayAgent.AbstractHandleUserRegistrationResponseState.__init__(self,
                                                                                          telegram_api_token)

    def create_check_user_registration_state(self, messaging_platform_api_token: str) -> \
            AbstractEchoGatewayAgent.AbstractCheckUserRegistrationState:
        return TelegramGatewayAgent.CheckUserRegistrationState(messaging_platform_api_token)

    def create_handle_user_registration_response_state(self, messaging_platform_api_token: str) -> \
            AbstractEchoGatewayAgent.AbstractHandleUserRegistrationResponseState:
        return TelegramGatewayAgent.HandleUserRegistrationResponseState(messaging_platform_api_token)
