from abc import ABC
from datetime import datetime
from typing import Optional

from mongoengine import Document

from common.database.abstract_suggestion_event import AbstractSuggestionEvent
from common.database.mongo_db import models


class MongoDBSuggestionEventMixin(AbstractSuggestionEvent, ABC):
    """MongoDB Mixin class to automatically implement the AbstractSuggestionEvent specified behaviour"""

    def __init__(self, _parent_obj: Document, _suggestion_event_mongo_db_obj: models.AbstractSuggestionEvent):
        self._parent_obj: Document = _parent_obj
        self._suggestion_event_mongo_db_obj: models.AbstractSuggestionEvent = _suggestion_event_mongo_db_obj

    @property
    def datetime(self) -> datetime:
        return self._suggestion_event_mongo_db_obj.datetime

    @datetime.setter
    def datetime(self, new_value: datetime):
        self._suggestion_event_mongo_db_obj.datetime = new_value
        self._parent_obj.save()

    @property
    def suggestion_message_id(self) -> Optional[str]:
        return self._suggestion_event_mongo_db_obj.suggestion_message_id

    @suggestion_message_id.setter
    def suggestion_message_id(self, new_value: str):
        self._suggestion_event_mongo_db_obj.suggestion_message_id = new_value
        self._parent_obj.save()

    @property
    def suggestion_usefulness(self) -> Optional[str]:
        return self._suggestion_event_mongo_db_obj.suggestion_usefulness

    @suggestion_usefulness.setter
    def suggestion_usefulness(self, new_value: str):
        self._suggestion_event_mongo_db_obj.suggestion_usefulness = new_value
        self._parent_obj.save()
