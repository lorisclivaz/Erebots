import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from common.database.mongo_db.models import Strategy
from common.database.mongo_db.persuation.model.strategy import MongoDBStrategy
from common.database.persuation.dao import AbstractStrategyDAO
from common.database.persuation.model.abstract_strategy import AbstractStrategy

logger = logging.getLogger(__name__)


class MongoDBStrategyDAO(AbstractStrategyDAO, MongoDBDAOMixin[MongoDBStrategy]):
    """Actual implementation for mongoDB of the Strategy Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, Strategy)

    def wrap_mongo_db_object(self, mongo_db_object: Strategy) -> MongoDBStrategy:
        return MongoDBStrategy(mongo_db_object)

    def insert(self, new_strategy: AbstractStrategy) -> AbstractStrategy:
        to_insert_strategy = Strategy.from_json(new_strategy.to_json_string())
        to_insert_strategy.save()
        return MongoDBStrategy(to_insert_strategy)
