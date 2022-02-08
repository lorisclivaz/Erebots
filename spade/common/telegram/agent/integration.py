import logging
from typing import Union, Optional

from aiogram import types
from aiogram.utils.emoji import demojize
from spade.agent import Agent
from spade.message import Message

from common.agent.utils import mas_message_pre_processing
from common.chat.message.factory import ChatMessageFactory
from common.chat.message.types import ChatMessage
from common.chat.platform.types import ChatPlatform

TELEGRAM_SENDER_NAME = "TelegramBotScript"

logger = logging.getLogger(__name__)


def forward_chat_message(message: Union[types.Message, types.CallbackQuery], to_agent: Agent):
    """Forwards received commands to provided Agent"""

    preprocessed_telegram_message = preprocess_and_label_telegram_message(message)
    logger.debug(preprocessed_telegram_message.strings_dictionary)

    mas_message = Message(
        to=str(to_agent.jid),
        sender=TELEGRAM_SENDER_NAME,
        body=demojize(message.text) if isinstance(message, types.Message) else message.data,
        metadata=preprocessed_telegram_message.strings_dictionary
    )
    to_agent.dispatch(mas_message)


def preprocess_and_label_telegram_message(message: Union[types.Message, types.CallbackQuery]) -> Optional[ChatMessage]:
    """Utility method which pre-processes and labels a telegram message"""

    stringyfied_telegram_message = mas_message_pre_processing(message)
    stringyfied_telegram_message[ChatPlatform.field_name()] = ChatPlatform.TELEGRAM.value
    return ChatMessageFactory.from_raw_strings_dictionary(stringyfied_telegram_message)
