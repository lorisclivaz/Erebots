import logging
from abc import ABC, abstractmethod
from typing import Mapping, Optional, Type

from mongoengine import Document

from common.database.abstract_dao import AbstractDAO, T

logger = logging.getLogger(__name__)


class MongoDBDAOMixin(AbstractDAO[T], ABC):
    """MongoDB Mixin class to automatically implement some AbstractDAO specified behaviour"""

    def __init__(self, mongo_db_document_class: Type[Document]):
        self._mongo_db_document_class: Type[Document] = mongo_db_document_class

    def find_by_id(self, object_id: str) -> Optional[T]:
        object_with_id = self._mongo_db_document_class.objects().with_id(object_id)
        return self.wrap_mongo_db_object(object_with_id)

    def find_by(self, **kwargs) -> Mapping[str, T]:
        documents = self._mongo_db_document_class.objects(**kwargs)
        if not documents:
            logger.info(f" No documents in MongoDB corresponding to filter: `{str(kwargs)}`")
            return {}
        else:
            return {str(document.id): self.wrap_mongo_db_object(document) for document in documents}

    def count(self) -> int:
        return self._mongo_db_document_class.objects.count()

    def delete_by_id(self, object_id: str) -> bool:
        object_with_id = self._mongo_db_document_class.objects().with_id(object_id)
        object_with_id.delete()
        return True

    @abstractmethod
    def wrap_mongo_db_object(self, mongo_db_object: Document) -> T:
        """Template method called when wrapping the mongo_db object is needed"""
        pass
