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

    FIRST_NAME = ("covid19_first_name", "[Covid19Project] First Name", AccessLevel.MANAGE)
    LANGUAGE = ("covid19_language", "[Covid19Project] Language", AccessLevel.MANAGE)
    AGE = ("covid19_age", "[Covid19Project] Age Range", AccessLevel.MANAGE)
    SEX = ("covid19_sex", "[Covid19Project] Sex", AccessLevel.MANAGE)
    FAVOURITE_SPORT_DAYS = ("covid19_favourite_sport_days", "[Covid19Project] Favourite Sport Days", AccessLevel.MANAGE)
    GOALS = ("covid19_goals", "[Covid19Project] Goal IDs", AccessLevel.MANAGE)
    CURRENT_QUESTION = ("covid19_current_question", "[Covid19Project] Current Question ID", AccessLevel.MANAGE)
    CURRENT_QUESTION_ANSWER = (
        "covid19_current_question_answer", "[Covid19Project] Current Question Answer", AccessLevel.MANAGE
    )
    SPORT_SESSIONS = ("covid19_sport_sessions", "[Covid19Project] Sport Session", AccessLevel.MANAGE)
    CHAT_MESSAGES = ("covid19_chat_messages", "[Covid19Project] Exchanged Chat Messages", AccessLevel.MANAGE)
