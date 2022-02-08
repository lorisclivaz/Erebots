from dataclasses import dataclass
from typing import Optional

from bson import json_util

from common.database.abstract_localized_object import AbstractLocalizedObject


@dataclass
class LocalizedObjectBeanMixin(AbstractLocalizedObject):
    """A bean Mixin class to automatically implement the AbstractSuggestionMessage specified behaviour"""

    text_en: str
    text_it: Optional[str] = None
    text_fr: Optional[str] = None
    text_de: Optional[str] = None

    def text_en(self) -> str:
        return self.text_en

    def to_json_string(self) -> str:
        return json_util.dumps({
            'text_en': self.text_en,
            'text_it': self.text_it,
            'text_fr': self.text_fr,
            'text_de': self.text_de,
        })
