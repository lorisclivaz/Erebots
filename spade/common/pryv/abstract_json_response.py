from abc import ABC
from typing import Union

from bson import json_util

from common.database.json_convertible import AbstractJsonConvertible


class AbstractJsonResponse(AbstractJsonConvertible, ABC):
    """Abstract class representing a Json response from a rest web service"""

    def __init__(self, json_representation: Union[str, dict]):
        self.internal_json: dict = (
            json_util.loads(json_representation) if isinstance(json_representation, str)
            else json_representation
        )

    def to_json_string(self) -> str:
        return json_util.dumps(self.internal_json)
