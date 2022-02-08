import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from echo.common.database.mongo_db.models import UnreadMessage
from echo.common.database.mongo_db.user.model.unread_message import (
    MongoDBUnreadMessage
)
from echo.common.database.user.daos import AbstractUnreadMessageDAO
from echo.common.database.user.model.abstract_unread_message import (
    AbstractUnreadMessage
)

logger = logging.getLogger(__name__)


class MongoDBUnreadMessageDAO(AbstractUnreadMessageDAO, MongoDBDAOMixin[MongoDBUnreadMessage]):
    """Actual implementation for mongoDB of the UnreadMessage Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, UnreadMessage)

    def wrap_mongo_db_object(self, mongo_db_object: UnreadMessage) -> MongoDBUnreadMessage:
        return MongoDBUnreadMessage(mongo_db_object)

    def insert(self, unread_message: AbstractUnreadMessage) -> AbstractUnreadMessage:
        to_insert_question_to_exercise_set_mapping = UnreadMessage.from_json(unread_message.to_json_string())
        to_insert_question_to_exercise_set_mapping.save()
        return MongoDBUnreadMessage(to_insert_question_to_exercise_set_mapping)
