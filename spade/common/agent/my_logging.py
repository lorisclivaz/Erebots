import logging

from spade.agent import Agent

from common.utils import my_logging

logger = logging.getLogger(__name__)


def log(from_agent: Agent, to_log_message, _logger=logger, _level=logging.INFO):
    """Utility function to log messages inside agents"""

    _logger.log(_level, f"[{from_agent.name}] {str(to_log_message)}")


def log_exception(from_agent: Agent, _logger=logger):
    """Utility function to log exceptions inside agents"""

    my_logging.log_exception(_logger, f"[{from_agent.name}] ")


def log_agent_contacts(agent: Agent, _logger=logger, _level=logging.INFO):
    """Utility function to log agent contacts list"""
    log(agent, f"Contacts List: {agent.presence.get_contacts()}", _logger, _level)
