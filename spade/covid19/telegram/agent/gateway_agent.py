import logging

from common.agent.my_logging import log, log_agent_contacts
from common.telegram.mixins import TelegramMixin
from covid19.common.agent.agents.abstract_covid19_gateway_agent import AbstractCovid19GatewayAgent
from covid19.common.database.connection_manager import AbstractCovid19ConnectionManager

logger = logging.getLogger(__name__)


class TelegramGatewayAgent(AbstractCovid19GatewayAgent):
    """The Telegram Gateway Agent between Telegram and the Multi-Agent System for Covid19 project"""

    def __init__(self, jid, password, telegram_sender_name: str, telegram_api_token: str,
                 db_connection_manager: AbstractCovid19ConnectionManager):
        super().__init__(jid, password, telegram_sender_name, telegram_api_token, db_connection_manager)

    async def setup(self):
        await super().setup()
        log(self, "TelegramGatewayAgent started.", logger)
        log_agent_contacts(self, logger)

    class CheckUserRegistrationState(
        TelegramMixin,
        AbstractCovid19GatewayAgent.AbstractCheckUserRegistrationState
    ):
        """The concrete registration checking state using TelegramMixin"""

        STATE_NAME = "CheckUserRegistrationState"

        def __init__(self, telegram_api_token: str):
            # with multiple inheritance all constructors must be called explicitly
            super().__init__(telegram_api_token)
            AbstractCovid19GatewayAgent.AbstractCheckUserRegistrationState.__init__(self, telegram_api_token)

    class HandleUserRegistrationResponseState(
        TelegramMixin,
        AbstractCovid19GatewayAgent.AbstractHandleUserRegistrationResponseState
    ):
        """The concrete response handling state"""

        STATE_NAME = "HandleUserRegistrationResponseState"

        def __init__(self, telegram_api_token: str):
            # with multiple inheritance all constructors must be called explicitly
            super().__init__(telegram_api_token)
            AbstractCovid19GatewayAgent.AbstractHandleUserRegistrationResponseState.__init__(self,
                                                                                             telegram_api_token)

    def create_check_user_registration_state(self, messaging_platform_api_token: str) -> \
            AbstractCovid19GatewayAgent.AbstractCheckUserRegistrationState:
        return TelegramGatewayAgent.CheckUserRegistrationState(messaging_platform_api_token)

    def create_handle_user_registration_response_state(self, messaging_platform_api_token: str) -> \
            AbstractCovid19GatewayAgent.AbstractHandleUserRegistrationResponseState:
        return TelegramGatewayAgent.HandleUserRegistrationResponseState(messaging_platform_api_token)
