import logging
import os
from pathlib import Path
from typing import Optional, List, Tuple, Callable

from spade.message import Message

from common.agent.agents.abstract_doctor_agent import AbstractDoctorAgent
from common.agent.agents.custom_metadata_fields import MasMessageMetadataFields, MasMessagePerformatives
from common.agent.my_logging import log, log_agent_contacts
from common.agent.web.controllers import OBJECT_ID_URL_MATCHER_STRING
from common.agent.web.utils import (
    add_get_raw_file, add_get_raw_controller, add_post_raw_controller, add_get_raw_files_in_folder
)
from common.chat.language_enum import Language
from common.chat.message.types import ChatMessage
from common.chat.platform.types import ChatPlatform
from common.custom_chat.client_notification_manager import ClientNotificationManager
from common.pryv.api_wrapper import PryvAPI
from echo.common.agent.agents.doctor.app_controllers import (
    create_app_login_controller, create_get_status_controller, create_credentials_checker_controller,
    create_message_sender_info_controller, create_user_messages_controller, create_user_language_controller,
    create_webapp_serving_controller, create_user_unread_messages_controller, API_MOUNT_POINT
)
from echo.common.database.connection_manager import AbstractEchoConnectionManager
from echo.common.database.user.daos import AbstractUserDAO
from echo.common.database.user.factory import UserFactory
from echo.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)

WEB_PAGE_ROOT = os.path.normpath(os.path.join("echo", "agent_web_pages", "doctor_agent", "build"))
"""The path to DoctorAgent web page root"""


class DoctorAgent(AbstractDoctorAgent):
    """The DoctorAgent is in charge of managing all the user data"""

    def __init__(self, jid, password,
                 gateway_agents_jids: List[str],
                 default_platform_and_token: Tuple[ChatPlatform, str],
                 connection_manager: AbstractEchoConnectionManager,
                 web_page_server_hostname: str,
                 web_page_server_port: str):
        super().__init__(jid, password, gateway_agents_jids)

        self.default_platform_and_token = default_platform_and_token
        self.connection_manager = connection_manager
        self.web_page_server_hostname = web_page_server_hostname
        self.web_page_server_port = web_page_server_port

    async def setup(self):
        await super().setup()

        log(self, "DoctorAgent started.", logger)
        log_agent_contacts(self, logger)

        # connect to DB
        self.connection_manager.connect_to_db()

        _start_web_server(self, self.connection_manager, str(os.path.abspath(WEB_PAGE_ROOT)))

    class HandleGatewayDataRequestState(AbstractDoctorAgent.AbstractHandleGatewayDataRequestState):
        """The state in charge of managing data requests coming from other agents"""

        STATE_NAME = "HandleGatewayDataRequestState"

        def get_connection_manager(self) -> AbstractEchoConnectionManager:
            return self.agent.connection_manager

        async def retrieve_requested_data(
                self,
                mas_message: Message,
                chat_message: ChatMessage,
                connection_manager: AbstractEchoConnectionManager
        ) -> Optional[AbstractUser]:

            user_dao = connection_manager.get_user_dao()
            result_user: Optional[AbstractUser] = None

            # Try to find the user by messaging platform ID, first
            if chat_message.chat_platform == ChatPlatform.TELEGRAM:
                result_user = await self._find_user_by_messaging_platform_id(
                    chat_message,
                    lambda messaging_platform_id: list(user_dao.find_by(telegram_id=messaging_platform_id).values())
                )
            elif chat_message.chat_platform == ChatPlatform.CUSTOM_CHAT:
                result_user = await self._find_user_by_messaging_platform_id(
                    chat_message,
                    lambda messaging_platform_id: list(user_dao.find_by(custom_chat_id=messaging_platform_id).values())
                )

            if result_user:
                # If user found directly with platform ID, return it
                return result_user

            else:  # Reaching this point means that a new user should be created

                _first_name: Optional[str] = chat_message.sender_first_name
                _language: Optional[Language] = chat_message.sender_locale

                log(self.agent, f"A new user will be created...", logger)

                msg = mas_message.make_reply()
                msg.metadata[MasMessageMetadataFields.PERFORMATIVE.value] = MasMessagePerformatives.INFORM.value
                msg.body = f"Creating a new user profile for {_first_name}"
                await self.send(msg)

                new_user = UserFactory.new_user(first_name=_first_name, language=_language)
                return user_dao.insert(new_user)

        async def _find_user_by_messaging_platform_id(
                self,
                chat_message: ChatMessage,
                finder_function: Callable[[str], List[AbstractUser]]
        ) -> Optional[AbstractUser]:
            """Utility method to find a user by messaging platform ID"""

            _sender_id = chat_message.sender_id
            users = finder_function(_sender_id)

            if len(users) == 1:
                return users[0]

            if len(users) > 1:  # More than one user with same messaging platform ID -> data error
                for p in users:
                    log(self.agent, f"{p.to_json_string()}", logger, logging.ERROR)

                raise RuntimeError(f"Retrieving user by {chat_message.chat_platform.value} ID `{_sender_id}`, "
                                   f"results in multiple users!!")

            return None

    def create_default_fsm_state(self) -> HandleGatewayDataRequestState:
        return DoctorAgent.HandleGatewayDataRequestState()


def _build_web_site(web_site_sources_path: Path):
    """A function to build a web site from python using npm"""
    pass  # TODO 06/04/2020: build web folder with NPM


def _start_web_server(agent: DoctorAgent, connection_manager: AbstractEchoConnectionManager, page_root: str):
    """Utility function to wrap server related initialization code"""

    user_dao: AbstractUserDAO = connection_manager.get_user_dao()
    pryv_api: PryvAPI = PryvAPI(connection_manager.pryv_server_domain)

    index_file = "index.html"

    add_get_raw_file(agent, "/", os.path.join(page_root, index_file))
    add_get_raw_controller(agent, "/webapp", create_webapp_serving_controller(f"webapp/{index_file}"))

    app_api_mount_point = f"{API_MOUNT_POINT}/app"
    add_get_raw_controller(
        agent, f"{app_api_mount_point}/server_status", create_get_status_controller()
    )
    add_get_raw_controller(
        agent, f"{app_api_mount_point}/login_page_url", create_app_login_controller(user_dao, pryv_api)
    )
    add_get_raw_controller(
        agent, f"{app_api_mount_point}/credential_check", create_credentials_checker_controller(user_dao, pryv_api)
    )
    add_get_raw_controller(
        agent, f"{app_api_mount_point}/message_sender_info", create_message_sender_info_controller(user_dao)
    )
    add_get_raw_controller(
        agent, f"{app_api_mount_point}/user_messages", create_user_messages_controller(user_dao)
    )
    add_get_raw_controller(
        agent, f"{app_api_mount_point}/user_unread_messages",
        create_user_unread_messages_controller(
            user_dao,
            ClientNotificationManager.get_instance(connection_manager.get_unread_message_dao())
        )
    )
    add_post_raw_controller(
        agent, f"{app_api_mount_point}/user/{{{OBJECT_ID_URL_MATCHER_STRING}}}/language",
        create_user_language_controller(user_dao)
    )

    to_serve_folder = Path(os.path.join(Path(__file__).parent, page_root))
    if not to_serve_folder.exists():
        log(agent, f"Folder `{to_serve_folder}` does not exist", logger)
        _build_web_site(Path(page_root).parent)
    else:
        log(agent, f"Will serve statically all files present in `{to_serve_folder}`", logger)
        add_get_raw_files_in_folder(agent, str(to_serve_folder))

        agent.web.start(
            hostname=agent.web_page_server_hostname,
            port=agent.web_page_server_port,
            templates_path=page_root
        )
