import datetime
import logging
from typing import Optional, Callable, List

from spade.behaviour import PeriodicBehaviour, FSMBehaviour

from common.agent.behaviour.abstract_fsm_state_behaviours import AbstractWaitForMessageState
from common.agent.my_logging import log
from common.agent.presence_utils import find_contact_by_partial_jid, subscribe_to

logger = logging.getLogger(__name__)


class TrySubscriptionToAgentBehaviour(PeriodicBehaviour):
    """Behaviour to try the subscription to given agent, until success"""

    def __init__(self, period: float, to_subscribe_agent_jid: str, start_at: datetime.datetime = None):
        super().__init__(period, start_at)
        self.to_subscribe_agent_jid = to_subscribe_agent_jid

    async def run(self):
        present_contact: Optional[str] = find_contact_by_partial_jid(self.to_subscribe_agent_jid, self.presence)
        if not present_contact:
            log(self.agent, f"Not found {self.to_subscribe_agent_jid} in contacts, trying to subscribe to it...",
                logger)
            subscribe_to(self.agent, self.to_subscribe_agent_jid, logger)
        else:
            self.kill(f"The {self.to_subscribe_agent_jid} contact is present in roaster.")


class WaitForMessageFSMBehaviour(FSMBehaviour):
    """The main FSM agent behaviour, by default will wait for messages to handle cyclically"""

    def __init__(self, initial_wait_for_message_creator: Callable[[], AbstractWaitForMessageState]):
        super().__init__()

        self.configure_fsm(initial_wait_for_message_creator)

    def configure_fsm(self, initial_wait_for_message_state_creator: Callable[[], AbstractWaitForMessageState]):
        """
        An overridable method to configure differently the FSM behaviour

        :param initial_wait_for_message_state_creator:
        The function needed to create the initial/default State of the FSM

        Default FSM behaviour is an endless loop, cycling to the initial/default behaviour, waiting for new messages
        """

        initial_default_state = initial_wait_for_message_state_creator()

        self.add_state(
            initial_default_state.STATE_NAME,
            initial_default_state,
            initial=True
        )
        self.add_transition(
            source=initial_default_state.STATE_NAME,
            dest=initial_default_state.STATE_NAME
        )

    def add_transitions_from_list(self, ordered_state_names: List[str]):
        """Utility method to quickly add transitions, specifying the path of states."""

        states_count = len(ordered_state_names)
        if states_count > 2:

            for index, state_name in enumerate(ordered_state_names):
                if index + 1 < states_count:
                    self.add_transition(state_name, ordered_state_names[index + 1])

    def add_waterfall_transitions_from_list(self,
                                            initial_state_name: str,
                                            ordered_state_names: List[str],
                                            every_state_self_transition: bool = True,
                                            last_to_initial_state_transition: bool = True):
        """
        Utility method to quickly add waterfall transitions, specifying the state progression

        "Waterfall" means that from each state you can reach all subsequent ones, but can't go back

        Optionally every state in "ordered_state_names" can have a self transition
        Optionally the last state can be connected back to the initial state
        """

        for index, state_name in enumerate([initial_state_name, *ordered_state_names]):
            for next_state_name in ordered_state_names[index:]:
                self.add_transition(state_name, next_state_name)

                if index == 0 and every_state_self_transition:
                    self.add_transition(next_state_name, next_state_name)

        if last_to_initial_state_transition:
            self.add_transition(ordered_state_names[-1], initial_state_name)
