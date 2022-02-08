from mongoengine import (
    StringField, BooleanField
)

from common.database.mongo_db.models import BasicUser
from common.pryv.model import AccessLevel
from common.utils.enums import ValuesMixin


class User(BasicUser):
    """Actual model class for user data stored in mongo_db"""

    telegram_id = StringField()
    custom_chat_id = StringField()
    pryv_endpoint = StringField()
    registration_completed = BooleanField(default=False)

    meta = {
        "strict": False,
        'ordering': ['-last_interaction']
    }


class PryvStoredData(ValuesMixin):
    """Enum class with all permissions requested to the user"""

    FIRST_NAME = ("echo_first_name", "[EchoProject] First Name", AccessLevel.MANAGE)
    LANGUAGE = ("echo_language", "[EchoProject] Language", AccessLevel.MANAGE)
    CHAT_MESSAGES = ("echo_chat_messages", "[EchoProject] Exchanged Chat Messages", AccessLevel.MANAGE)
    CHAT_IMAGES = ("echo_chat_images", "[EchoProject] Exchanged Chat Images", AccessLevel.MANAGE)
