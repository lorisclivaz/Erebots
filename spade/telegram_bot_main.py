import logging
import os

from aiogram import executor

from common.telegram.agent.integration import TELEGRAM_SENDER_NAME
from common.telegram.bot import BotHandlersWrapper
from common.utils.evironment import get_env_variable_or_error
from common.utils.my_logging import log_exception
from common.working_contexts import WorkingContext

logger = logging.getLogger(__name__)

WORKING_CONTEXT = os.environ.get("CURRENT_WORKING_CONTEXT", WorkingContext.ECHO.value)
"""The working context in which the GatewayAgent should operate"""

if __name__ == '__main__':
    if WORKING_CONTEXT in WorkingContext.values():  # check for legal working context

        if WORKING_CONTEXT == WorkingContext.COVID19.value:
            from covid19.common.bootstrap_agent_names import TELEGRAM_GATEWAY_JID
            from covid19.common.database.mongo_db_pryv_hybrid.connection import (
                MongoDBAndPryvHybridConnectionManager, DATABASE_NAME, CONNECTION_URI
            )
            from common.pryv.server_domain import PRYV_SERVER_DOMAIN
            from covid19.telegram.agent.gateway_agent import TelegramGatewayAgent

            bot_api_token = get_env_variable_or_error("COVID19_TELEGRAM_BOT_API_TOKEN")

            telegram_gateway_agent = TelegramGatewayAgent(
                jid=TELEGRAM_GATEWAY_JID,
                password="telegram_agent_psw",
                telegram_sender_name=TELEGRAM_SENDER_NAME,
                telegram_api_token=bot_api_token,
                db_connection_manager=MongoDBAndPryvHybridConnectionManager(
                    DATABASE_NAME, CONNECTION_URI, PRYV_SERVER_DOMAIN
                )
            )

        else:
            telegram_gateway_agent = None
            bot_api_token = None
            logger.error(f"Working context not recognized!!!")

        bot_handlers = BotHandlersWrapper(bot_api_token, telegram_gateway_agent, WORKING_CONTEXT)

        future = telegram_gateway_agent.start()
        future.result()  # wait for the agent to be online before pulling messages from Telegram

        try:
            while True:  # This loop restarts the Telegram Bot if an exception occurs during polling
                try:
                    executor.start_polling(bot_handlers.telegram_dispatcher, skip_updates=True)
                except KeyboardInterrupt:
                    logger.info(" KeyboardInterrupt: Stopping Telegram Bot...")
                    break
                except:
                    log_exception()
                    logger.info(" Restarting Telegram Bot after exception...")
        finally:
            telegram_gateway_agent.stop()
            logger.warning(" Telegram bot quit.")
    else:
        logger.error(f" Currently selected working context `{WORKING_CONTEXT}` is not supported")
