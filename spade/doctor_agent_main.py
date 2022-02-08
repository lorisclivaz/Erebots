import logging
import os
import time

from common.agent.web.server_address import WEB_SERVER_INTERNAL_IP, WEB_SERVER_INTERNAL_PORT
from common.chat.platform.types import ChatPlatform
from common.utils.evironment import get_env_variable_or_error
from common.working_contexts import WorkingContext

logger = logging.getLogger(__name__)

WORKING_CONTEXT = os.environ.get("CURRENT_WORKING_CONTEXT", WorkingContext.COVID19.value)
"""The working context in which the DoctorAgent should operate"""

DOCTOR_AGENT_NAME = f"{WORKING_CONTEXT}_doctor_agent"

if __name__ == '__main__':
    if WORKING_CONTEXT in WorkingContext.values():  # check for legal working context

        if WORKING_CONTEXT == WorkingContext.COVID19.value:
            from covid19.common.agent.agents.doctor.doctor_agent import DoctorAgent
            from covid19.common.bootstrap_agent_names import ALL_PLATFORMS_GATEWAY_AGENTS_JIDS
            from covid19.common.database.mongo_db_pryv_hybrid.connection import (
                MongoDBAndPryvHybridConnectionManager, DATABASE_NAME, CONNECTION_URI
            )
            from covid19.common.xmpp_server import XMPP_SERVER_ADDRESS
            from common.pryv.server_domain import PRYV_SERVER_DOMAIN

            bot_api_token = get_env_variable_or_error("COVID19_TELEGRAM_BOT_API_TOKEN")

            doctor_agent = DoctorAgent(
                jid=f"{DOCTOR_AGENT_NAME}@{XMPP_SERVER_ADDRESS}",
                password=DOCTOR_AGENT_NAME,
                gateway_agents_jids=ALL_PLATFORMS_GATEWAY_AGENTS_JIDS,
                default_platform_and_token=(ChatPlatform.TELEGRAM, bot_api_token),
                connection_manager=MongoDBAndPryvHybridConnectionManager(
                    DATABASE_NAME, CONNECTION_URI, PRYV_SERVER_DOMAIN
                ),
                web_page_server_hostname=WEB_SERVER_INTERNAL_IP,
                web_page_server_port=WEB_SERVER_INTERNAL_PORT
            )
        else:
            doctor_agent = None
            logger.error(f"Working context not recognized!!!")

        future = doctor_agent.start()
        future.result()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
        doctor_agent.stop()

    else:
        logger.error(f" Currently selected working context `{WORKING_CONTEXT}` is not supported")
