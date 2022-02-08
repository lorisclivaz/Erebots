import logging
import os

logger = logging.getLogger(__name__)


def get_env_variable_or_error(variable_name: str) -> str:
    """Utility function to get an environment variable by name, or raise error if not present"""

    variable = os.environ.get(variable_name)

    if not variable:
        err_msg = f" {variable_name} env variable not found."
        logger.error(err_msg)
        raise EnvironmentError(err_msg)

    return variable
