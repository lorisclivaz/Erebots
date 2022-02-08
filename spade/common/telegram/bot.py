import logging

from aiogram import types, Bot, Dispatcher
from aiogram.types import ContentTypes
from emoji import demojize
from spade.agent import Agent

from common.telegram.agent.integration import forward_chat_message
from common.utils.reflection import add_method_to_class, get_current_function_name

logger = logging.getLogger(__name__)


class BotHandlersWrapper:
    """A class wrapping Telegram messages handlers"""

    def __init__(self, telegram_api_token: str, gateway_agent: Agent, bot_context: str):
        self.telegram_dispatcher = Dispatcher(Bot(telegram_api_token))

        # Handlers are evaluated in order, executing only the first matching

        add_method_to_class(
            self.telegram_dispatcher.message_handler(content_types=ContentTypes.TEXT)(
                create_receive_known_command_handler(gateway_agent)
            ),
            BotHandlersWrapper,
            f"{bot_context}_received_known_command"
        )

        add_method_to_class(
            self.telegram_dispatcher.message_handler(content_types=ContentTypes.all())(
                create_receive_non_command_handler(gateway_agent)
            ),
            BotHandlersWrapper,
            f"{bot_context}_received_non_command"
        )

        add_method_to_class(
            self.telegram_dispatcher.callback_query_handler(lambda callback_query: True)(
                create_callback_handler(gateway_agent)
            ),
            BotHandlersWrapper,
            f"{bot_context}_callback_handler"
        )


def create_receive_known_command_handler(gateway_agent: Agent):
    """
    Creates a Telegram bot Handler function to be used to handle TEXT messages from telegram;

    Forwards the Telegram message as is to the gateway_agent
    """

    async def received_known_command(message: types.Message):
        """This handler will be called when user sends text"""

        logger.info(f" {get_current_function_name()}: `{demojize(message.text)}` from `{message.chat.first_name}`"
                    f" with ID `{message.message_id}`")
        forward_chat_message(message, gateway_agent)

    return received_known_command


def create_receive_non_command_handler(gateway_agent: Agent):
    """
    Creates a Telegram bot Handler function to be used to handle non TEXT messages from telegram;

    Manipulates the received Telegram message (initializing/replacing the text field with the content type of the
    message) and forwards it to the gateway_agent
    """

    async def received_non_command(message: types.Message):
        """This handler will be called when user sends something that's not text"""

        logger.info(f" {get_current_function_name()}: `{message.content_type}` from `{message.chat.first_name}`")
        message.text = str(message.content_type)
        forward_chat_message(message, gateway_agent)

    return received_non_command


def create_callback_handler(gateway_agent: Agent):
    """
    Creates a Telegram bot Handler function to be used to handle Callback queries from telegram;

    Forwards the Telegram callback_query as is to the gateway_agent
    """

    async def callback_handler(callback_query: types.CallbackQuery):
        """This handler will forward the callback data to the Agent"""

        logger.info(
            f" {get_current_function_name()}: `{callback_query.data}` from `{callback_query.message.chat.first_name}`"
        )
        forward_chat_message(callback_query, gateway_agent)

    return callback_handler
