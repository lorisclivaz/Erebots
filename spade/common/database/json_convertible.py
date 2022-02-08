import json
from abc import ABC, abstractmethod
from typing import Any, Optional, Mapping


class AbstractJsonConvertible(ABC):
    """A class representing an object which is JSON convertible"""

    def to_json(self) -> Mapping[str, Optional[Any]]:
        """Converts this data structure to JSON"""
        return json.loads(self.to_json_string())

    @abstractmethod
    def to_json_string(self) -> str:
        """Converts this data structure to a JSON string"""
        pass

    def __str__(self):
        return self.to_json_string()
