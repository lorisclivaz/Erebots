import logging
from asyncio import coroutine
from pathlib import Path
from typing import TypeVar, Optional

from spade.agent import Agent

from common.agent.web.controllers import (
    create_static_file_controller, create_objects_controller, create_object_count_controller, create_object_controller,
    OBJECT_ID_URL_MATCHER_STRING
)
from common.agent.web.mime_type_utils import extension_to_mime_type
from common.database.abstract_dao import AbstractDAO
from common.database.cache.abstract_cache_dao import AbstractCacheDAO
from common.utils.lists import flatten_list

logger = logging.getLogger(__name__)


def add_get_raw_controller(agent: Agent, web_route: str, handling_controller: coroutine):
    """Add a route that sends back requested data through the provided controller"""

    agent.web.add_get(web_route, handling_controller, template=None, raw=True)


def add_get_raw_file(agent: Agent, web_route: str, file_path: str):
    """Add a route that sends back the specified file, without processing it as a template"""

    add_get_raw_controller(agent, web_route, create_static_file_controller(file_path))


def add_get_raw_files_in_folder(agent: Agent, folder_path: str, base_web_endpoint: str = ""):
    """Add multiple routes which send back the requested files inside a provided folder"""

    to_serve_file_extensions = [f"*.{file_type}" for file_type in extension_to_mime_type.keys()]

    to_serve_files = flatten_list([list(Path(folder_path).rglob(file_type)) for file_type in to_serve_file_extensions])
    logger.debug(f" List of files that will be served by {agent.jid}: {to_serve_files}")

    for file in to_serve_files:
        relative_path = str(file)[len(folder_path):]
        url_like = relative_path.replace("\\", "/")
        to_add_url = base_web_endpoint + url_like
        logger.debug(f" Will add {to_add_url}")
        add_get_raw_file(agent, to_add_url, file)


T = TypeVar('T')


def add_all_get_controllers(
        agent: Agent,
        api_mount_point: str,
        resource_name: str,
        object_dao: AbstractDAO[T],
        cache_dao: Optional[AbstractCacheDAO] = None
):
    """
    Utility method to add GET controllers (all, count, and single object) using provided DAOs, with optional caching
    """

    add_get_raw_controller(
        agent, f"{api_mount_point}/{resource_name}",
        create_objects_controller(object_dao, cache_dao)
    )
    add_get_raw_controller(
        agent, f"{api_mount_point}/{resource_name}/count",
        create_object_count_controller(object_dao)
    )
    add_get_raw_controller(
        agent, f"{api_mount_point}/{resource_name}/{{{OBJECT_ID_URL_MATCHER_STRING}}}",
        create_object_controller(object_dao)
    )


def add_post_raw_controller(agent: Agent, web_route: str, handling_controller: coroutine):
    """Add a route that handle received data through the provided controller"""

    agent.web.add_post(web_route, handling_controller, template=None, raw=True)
