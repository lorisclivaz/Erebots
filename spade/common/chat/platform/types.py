from common.utils.enums import ValuesMixin


class ChatPlatform(ValuesMixin):
    """Enumeration of chat platforms"""

    TELEGRAM = "telegram"
    """Telegram chat platform"""

    FACEBOOK_MESSENGER = "facebook_messenger"
    """Facebook messenger chat platform"""

    CUSTOM_CHAT = "custom_chat"
    """Custom chat platform"""

    @staticmethod
    def field_name():
        """Returns the field name related to this enumeration"""
        return "chat_platform"
