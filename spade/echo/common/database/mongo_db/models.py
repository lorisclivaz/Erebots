from mongoengine import (
    StringField, BooleanField, Document
)

from common.database.mongo_db.models import BasicUser


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


class UnreadMessage(Document):
    """Model class to represent a message directed to so some user"""

    recipient_id = StringField()
    message_json = StringField()
