import json
from datetime import datetime

from common.database.cache.model.abstract_cache_data import AbstractCacheData
from common.database.mongo_db.models import CacheData


class MongoDBCacheData(AbstractCacheData):
    """Actual implementation of Cache data retrieving data from MongoDB"""

    def __init__(self, _mongo_db_obj: CacheData):
        self._cache_data_mongodb_obj: CacheData = _mongo_db_obj

    @property
    def id(self) -> str:
        return self._cache_data_mongodb_obj.id

    @property
    def cache_data(self) -> str:
        return self._cache_data_mongodb_obj.cache_data

    @cache_data.setter
    def cache_data(self, new_value: str):
        self._cache_data_mongodb_obj.cache_data = new_value
        self._cache_data_mongodb_obj.save()

    @property
    def timestamp(self) -> datetime:
        return self._cache_data_mongodb_obj.timestamp

    @timestamp.setter
    def timestamp(self, new_value: datetime):
        self._cache_data_mongodb_obj.timestamp = new_value
        self._cache_data_mongodb_obj.save()

    @property
    def cache_over_number(self) -> int:
        return self._cache_data_mongodb_obj.cache_over_number

    @cache_over_number.setter
    def cache_over_number(self, new_value: int):
        self._cache_data_mongodb_obj.cache_over_number = new_value
        self._cache_data_mongodb_obj.save()

    def to_json_string(self) -> str:
        return self._cache_data_mongodb_obj.to_json()
