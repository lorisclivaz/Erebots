from abc import ABC, abstractmethod
from typing import Optional

from common.database.cache.model.abstract_cache_data import AbstractCacheData


class AbstractCacheDAO(ABC):
    """An abstract Data Access Object for Cached data"""

    @abstractmethod
    def insert_cache(self, cache_data: AbstractCacheData):
        """Saves into the database the provided new cache entry"""
        pass

    @abstractmethod
    def find_by_id(self, cached_data_id: str) -> Optional[AbstractCacheData]:
        """Finds a cache data by ID; returns None if not found"""
        pass

    @abstractmethod
    def delete_cache_with_id(self, cache_data_id: str):
        """Deletes the cached data with certain ID"""
        pass
