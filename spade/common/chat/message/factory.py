import logging
from typing import Optional, Mapping

from common.chat.message.types import ChatMessage
from common.chat.platform.types import ChatPlatform
from common.custom_chat.messages import CustomChatMessage
from common.telegram.messages import TelegramMessage

logger = logging.getLogger(__name__)


class ChatMessageFactory:
    """A factory for ChatMessages"""

    @staticmethod
    def from_raw_strings_dictionary(strings_dictionary: Mapping[str, str]) -> Optional[ChatMessage]:
        """Factory method to create specific platform chat messages, returns None if message type not recognized"""

        current_platform = strings_dictionary[ChatPlatform.field_name()]
        chat_message: Optional[ChatMessage] = None

        if current_platform == ChatPlatform.TELEGRAM.value:
            chat_message = TelegramMessage.from_strings_dictionary(strings_dictionary)

        elif current_platform == ChatPlatform.FACEBOOK_MESSENGER.value:
            logger.warning(f" Not implemented facebook message creation")
        elif current_platform == ChatPlatform.CUSTOM_CHAT.value:
            chat_message = CustomChatMessage.from_strings_dictionary(strings_dictionary)
        else:
            logger.error(f" Cannot recognize the message platform, "
                         f"missing `{ChatPlatform.field_name()}` field in `{str(strings_dictionary)}`")

        return chat_message
