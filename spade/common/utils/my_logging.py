import logging

logger = logging.getLogger(__name__)


def log_exception(_logger=logger, prefix: str = ""):
    """Utility function to log current context exceptions"""

    import sys
    _logger.error(f" {prefix}Unexpected error: {sys.exc_info()[0]} {sys.exc_info()[1]}", exc_info=True)
