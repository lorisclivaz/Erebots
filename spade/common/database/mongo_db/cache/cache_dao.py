import logging
from typing import Optional

from common.database.cache.abstract_cache_dao import AbstractCacheDAO
from common.database.cache.model.abstract_cache_data import AbstractCacheData
from common.database.mongo_db.cache.model.cache_data import MongoDBCacheData
from common.database.mongo_db.models import CacheData

logger = logging.getLogger(__name__)


class MongoDBCacheDAO(AbstractCacheDAO):
    """Actual implementation for mongoDB of the cache data access object"""

    def insert_cache(self, cache_data: AbstractCacheData):
        new_cache_data = CacheData(
            id=cache_data.id,
            timestamp=cache_data.timestamp,
            cache_over_number=cache_data.cache_over_number,
            cache_data=cache_data.cache_data,
        )
        new_cache_data.save()
        return MongoDBCacheData(new_cache_data)

    def find_by_id(self, cached_data_id: str) -> Optional[AbstractCacheData]:
        cache_with_id = CacheData.objects(id=cached_data_id)
        if cache_with_id:
            return cache_with_id[0]
        else:
            return None

    def delete_cache_with_id(self, cache_data_id: str):
        cache_with_id: CacheData = CacheData.objects(id=cache_data_id).first()
        if cache_with_id:
            cache_with_id.delete()
        else:
            logger.warning(f" Trying to delete a non present cache object with ID `{cache_data_id}`")
