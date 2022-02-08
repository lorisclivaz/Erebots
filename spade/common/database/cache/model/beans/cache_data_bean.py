from dataclasses import dataclass
from datetime import datetime

from bson import json_util

from common.database.cache.model.abstract_cache_data import AbstractCacheData


@dataclass
class CacheDataBean(AbstractCacheData):
    """A bean class to create cache instances not directly bound to a database instance"""

    id: str
    cache_over_number: int
    cache_data: str
    timestamp: datetime

    def id(self) -> str:
        return self.id

    def cache_over_number(self) -> int:
        return self.cache_over_number

    def cache_data(self) -> str:
        return self.cache_data

    def timestamp(self) -> datetime:
        return self.timestamp

    def to_json_string(self) -> str:
        return json_util.dumps({
            'id': self.id,
            'timestamp': self.timestamp,
            'cache_over_number': self.cache_over_number,
            'cache_data': self.cache_data,
        })
