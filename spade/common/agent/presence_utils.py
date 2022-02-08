import logging
from typing import Optional

from aioxmpp import JID, Presence, PresenceType
from spade.agent import Agent
from spade.presence import PresenceManager

from common.agent.my_logging import log, log_agent_contacts

logger = logging.getLogger(__name__)


def setup_presence_manager(agent: Agent, _logger=logger):
    """Sets up the Presence manager to mutually subscribe two agents"""

    def on_subscribed(jid):
        log(agent, f"Agent {jid} has accepted the subscription.", _logger)
        log_agent_contacts(agent, _logger, logging.DEBUG)

    def on_subscribe(jid):
        log(agent, f"Agent {jid} asked for subscription. Let's approve it.", _logger)
        agent.presence.approve(jid)
        agent.presence.subscribe(jid)

    agent.presence.on_subscribe = on_subscribe
    agent.presence.on_subscribed = on_subscribed


def find_contact_by_partial_name(partial_name: str, presence_manager: PresenceManager) -> Optional[str]:
    """Utility function to take a JID which matches the given partial name, from the agent contact list"""

    for (jid, __) in presence_manager.get_contacts().items():
        if partial_name.lower() in jid.localpart.lower():
            return str(jid)


def find_contact_by_partial_jid(to_search_jid: str, presence_manager: PresenceManager) -> Optional[str]:
    """Utility function to take a JID which matches the given jid, from the agent contact list"""

    search_jid_str = str(to_search_jid).lower()
    for (jid, info_dict) in presence_manager.get_contacts().items():

        # I've found that the most complete representation of the JID "obscurely" resides in presence "from_" field
        if info_dict and info_dict.get('presence', None):
            contact_most_complete_jid = str(info_dict['presence'].from_).lower()
            if search_jid_str in contact_most_complete_jid and not _last_subscription_failed(info_dict):
                return str(jid)

        # If for some reason "info_dict" object is not available, fallback to te common JID string
        elif search_jid_str in f"{jid.localpart}@{jid.domain}".lower() and not _last_subscription_failed(info_dict):
            return str(jid)


def get_presence(jid: str, presence_manager: PresenceManager) -> Presence:
    """Utility method to gather the presence of an Agent"""

    actual_jid = JID.fromstr(str(jid))
    return presence_manager.get_contact(actual_jid).get('presence', Presence(type_=PresenceType.UNAVAILABLE))


def is_agent_available(jid: Optional[str], presence_manager: PresenceManager) -> bool:
    """Utility method to check if an agent is available"""

    return jid and get_presence(jid, presence_manager).type_ == PresenceType.AVAILABLE


def subscribe_to(agent: Agent, jid: str, _logger=logger):
    """Utility function to subscribe to an Agent JID if not already subscribed to"""

    string_jid = str(jid)
    for (already_present_jid, info_dict) in agent.presence.get_contacts().items():  # foreach contact
        if str(already_present_jid) == string_jid:  # if found the JID
            if not _last_subscription_failed(info_dict):  # if last subscription successful
                log(agent, f"The contact {string_jid} is already present in roaster", _logger)
                return  # do nothing
            else:  # if last subscription failed
                agent.presence.unsubscribe(jid)  # unsubscribe, to delete the failed contact subscription
                break  # continue to subscription

    log(agent, f"Trying to subscribe to {string_jid}", _logger)
    agent.presence.subscribe(jid)


def _last_subscription_failed(contact_info_dict: dict) -> bool:
    """Returns true if the subscription failed, false otherwise"""

    # If subscription field is 'none', then last subscription has failed, and the case must be treated like if
    #  there's no matching contact
    return contact_info_dict and contact_info_dict.get('subscription', None) == 'none'
