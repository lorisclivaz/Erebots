import logging
from abc import abstractmethod, ABC
from typing import List, Optional

from spade.message import Message
from spade.template import Template, ORTemplate

from common.agent.agents.custom_metadata_fields import MasMessageMetadataFields, MasMessagePerformatives
from common.agent.agents.my_abstract_agent import AbstractBaseFSMAgent
from common.agent.behaviour.abstract_fsm_state_behaviours import AbstractWaitForChatMessageState
from common.agent.behaviour.behaviours import TrySubscriptionToAgentBehaviour
from common.agent.my_logging import log, log_exception
from common.chat.message.types import ChatMessage
from common.database.connection_manager import AbstractConnectionManager
from common.database.json_convertible import AbstractJsonConvertible

logger = logging.getLogger(__name__)


class AbstractDoctorAgent(AbstractBaseFSMAgent, ABC):

    def __init__(self, jid, password, gateway_agents_jids: List[str]):
        super().__init__(jid, password)

        self.gateway_agents_jids = gateway_agents_jids

    async def setup(self):
        await super().setup()

        for a_gateway_agent_jid in self.gateway_agents_jids:
            self.add_behaviour(
                TrySubscriptionToAgentBehaviour(period=2, to_subscribe_agent_jid=a_gateway_agent_jid)
            )

    def create_fsm_behaviour_message_template(self) -> Optional[Template]:
        all_gateways_template = None
        for a_gateway_agent_jid in self.gateway_agents_jids:
            current_agent_template = Template(to=self.jid_str)
            current_agent_template.metadata[MasMessageMetadataFields.PERFORMATIVE.value] = \
                MasMessagePerformatives.REQUEST.value
            current_agent_template.metadata[MasMessageMetadataFields.SENDER.value] = a_gateway_agent_jid

            if all_gateways_template is None:
                all_gateways_template = current_agent_template
            else:
                all_gateways_template = ORTemplate(
                    all_gateways_template,
                    current_agent_template
                )

        return all_gateways_template

    class AbstractHandleGatewayDataRequestState(AbstractWaitForChatMessageState, ABC):
        """The abstract behaviour in charge of managing data requests coming from other agents"""

        STATE_NAME = "AbstractHandleGatewayDataRequestState"

        async def on_chat_message_received(self, mas_message: Message, chat_message: ChatMessage):
            log(self.agent, f"Received request from {mas_message.sender} for data about {mas_message.body}", logger)
            reply_message = mas_message.make_reply()
            try:
                connection_manager: AbstractConnectionManager = self.get_connection_manager()
                found_data: AbstractJsonConvertible = await self.retrieve_requested_data(
                    mas_message,
                    chat_message,
                    connection_manager
                )
                if not found_data:
                    reply_message.body = "{}"
                    reply_message.metadata[MasMessageMetadataFields.PERFORMATIVE.value] = \
                        MasMessagePerformatives.FAILURE.value
                    reply_message.metadata[MasMessageMetadataFields.FAIL_MESSAGE.value] = "Data not found"
                else:
                    log(self.agent, f"Successfully retrieved data: {found_data.to_json_string()}", logger)
                    reply_message.body = found_data.to_json_string()
                    reply_message.metadata[MasMessageMetadataFields.PERFORMATIVE.value] = \
                        MasMessagePerformatives.INFORM_RESULT.value
            except:
                log_exception(self.agent, logger)
                reply_message.body = "{}"
                reply_message.metadata[
                    MasMessageMetadataFields.PERFORMATIVE.value] = MasMessagePerformatives.FAILURE.value
                reply_message.metadata[MasMessageMetadataFields.FAIL_MESSAGE.value] = "Exception during search"

            await self.send(reply_message)

        @abstractmethod
        def get_connection_manager(self) -> AbstractConnectionManager:
            """Template method to retrieve the connection manager to be provided in retrieving data phase"""
            pass

        @abstractmethod
        async def retrieve_requested_data(
                self,
                mas_message: Message,
                chat_message: ChatMessage,
                connection_manager: AbstractConnectionManager
        ) -> Optional[AbstractJsonConvertible]:
            """Template method to retrieve the requested data, from DB"""
            pass

    @abstractmethod
    def create_default_fsm_state(self) -> AbstractHandleGatewayDataRequestState:
        """Template method to create the State which will answers to gateway agents, asking for user information"""
        pass
