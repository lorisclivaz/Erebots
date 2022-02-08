from datetime import datetime

from common.database.cache.model.abstract_cache_data import AbstractCacheData
from common.database.cache.model.beans.cache_data_bean import CacheDataBean


class CacheDataFactory:
    """A class containing factory methods for cache data"""

    @staticmethod
    def new_cache(
            _id: str,
            cache_over_number: int,
            cache_data: str,
            timestamp: datetime = None
    ) -> AbstractCacheData:
        """A factory method to create a new Cache data"""

        if timestamp is None:
            timestamp = datetime.now()

        return CacheDataBean(_id, cache_over_number, cache_data, timestamp)
