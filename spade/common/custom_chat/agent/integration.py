import json
import logging
from typing import Optional

import emoji
from spade.agent import Agent
from spade.message import Message

from common.agent.utils import mas_message_pre_processing
from common.chat.message.factory import ChatMessageFactory
from common.chat.message.types import ChatMessage
from common.chat.platform.types import ChatPlatform

CUSTOM_CHAT_SENDER_NAME = "CustomChatScript"

logger = logging.getLogger(__name__)


def forward_chat_message(message_json: str, to_agent: Agent):
    """Forwards received commands to provided Agent"""

    preprocessed_custom_chat_message = preprocess_and_label_custom_chat_message(message_json)
    logger.debug(preprocessed_custom_chat_message.strings_dictionary)

    mas_message = Message(
        to=str(to_agent.jid),
        sender=CUSTOM_CHAT_SENDER_NAME,
        body=emoji.demojize(preprocessed_custom_chat_message.message_text),
        metadata=preprocessed_custom_chat_message.strings_dictionary
    )
    to_agent.dispatch(mas_message)


def preprocess_and_label_custom_chat_message(message_json: str) -> Optional[ChatMessage]:
    """Utility method which pre-processes and labels a telegram message"""

    stringyfied_custom_chat_message = mas_message_pre_processing(json.loads(message_json))
    stringyfied_custom_chat_message[ChatPlatform.field_name()] = ChatPlatform.CUSTOM_CHAT.value
    return ChatMessageFactory.from_raw_strings_dictionary(stringyfied_custom_chat_message)
