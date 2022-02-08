from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bson import json_util

from common.chat.language_enum import Language
from common.database.user.abstract_user import AbstractBasicUser


@dataclass
class BasicUserBeanMixin(AbstractBasicUser):
    """A bean Mixin class to automatically implement the AbstractUser specified behaviour"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language: Optional[Language] = None
    last_interaction: datetime = datetime.min

    def to_json_string(self) -> str:
        return json_util.dumps({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'language': self.language.value if self.language else None,
            'last_interaction': self.last_interaction,
        })
