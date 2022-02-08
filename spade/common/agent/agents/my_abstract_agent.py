import logging
from abc import ABC, abstractmethod
from typing import Optional

from aioxmpp import PresenceState
from spade.agent import Agent
from spade.template import Template

from common.agent.behaviour.abstract_fsm_state_behaviours import AbstractWaitForMessageState
from common.agent.behaviour.behaviours import WaitForMessageFSMBehaviour
from common.agent.presence_utils import setup_presence_manager

logger = logging.getLogger(__name__)


class AbstractBaseAgent(Agent, ABC):
    """A base class for all the project agents, with common behaviour"""

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.jid_str = str(self.jid)

    async def setup(self):
        setup_presence_manager(self, logger)

        self.presence.set_presence(PresenceState(True))


class AbstractBaseFSMAgent(AbstractBaseAgent, ABC):
    """A base class for all project agents which will have a main FSM behaviour waiting for messages"""

    async def setup(self):
        await super().setup()

        self.add_behaviour(
            self.create_fsm_behaviour(),
            self.create_fsm_behaviour_message_template()
        )

    def create_fsm_behaviour(self) -> WaitForMessageFSMBehaviour:
        """A default method creating the FSM behaviour waiting for messages"""
        return WaitForMessageFSMBehaviour(self.create_default_fsm_state)

    @abstractmethod
    def create_default_fsm_state(self) -> AbstractWaitForMessageState:
        """Template method to create the agent default FSM State"""
        pass

    @abstractmethod
    def create_fsm_behaviour_message_template(self) -> Optional[Template]:
        """Template method, to create a template for the agent main FSM behaviour, or None if no template needed"""
        pass
