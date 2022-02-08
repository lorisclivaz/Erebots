from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bson import json_util

from common.database.abstract_suggestion_event import AbstractSuggestionEvent


@dataclass
class SuggestionEventBeanMixin(AbstractSuggestionEvent):
    """A bean Mixin class to automatically implement the AbstractSuggestionEvent specified behaviour"""

    datetime: datetime
    suggestion_message_id: Optional[str] = None
    suggestion_usefulness: Optional[str] = None

    def datetime(self) -> datetime:
        return self.datetime

    def to_json_string(self) -> str:
        return json_util.dumps({
            'datetime': self.datetime,
            'suggestion_message_id': self.suggestion_message_id,
            'suggestion_usefulness': self.suggestion_usefulness,
        })
