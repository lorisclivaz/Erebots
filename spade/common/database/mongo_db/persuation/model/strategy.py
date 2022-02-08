from typing import Optional

from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from common.database.mongo_db.models import Strategy
from common.database.persuation.model.abstract_strategy import AbstractStrategy


class MongoDBStrategy(AbstractStrategy, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractStrategy for MongoDB"""

    def __init__(self, _mongo_db_obj: Strategy):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        self._strategy_mongodb_obj: Strategy = _mongo_db_obj

    @property
    def name(self) -> Optional[str]:
        return self._strategy_mongodb_obj.name

    @name.setter
    def name(self, new_value: str):
        self._strategy_mongodb_obj.name = new_value
        self._strategy_mongodb_obj.save()

    @property
    def description(self) -> Optional[str]:
        return self._strategy_mongodb_obj.description

    @description.setter
    def description(self, new_value: str):
        self._strategy_mongodb_obj.description = new_value
        self._strategy_mongodb_obj.save()

    def to_json_string(self) -> str:
        return self._strategy_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, strategy_json: str):
        """Creates a MongoDBStrategy from a json string"""

        return cls(Strategy.from_json(strategy_json))
