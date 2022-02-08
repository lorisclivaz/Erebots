from mongoengine import Document

from common.database.abstract_object_with_id import AbstractObjectWithID


class MongoDBObjectWithIDMixin(AbstractObjectWithID):
    """MongoDB Mixin class to automatically implement the AbstractObjectWithID specified behaviour"""

    def __init__(self, _mongo_db_obj: Document):
        self._mongo_db_obj: Document = _mongo_db_obj

    @property
    def id(self) -> str:
        return str(self._mongo_db_obj.id)
