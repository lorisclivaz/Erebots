from common.database.abstract_object_with_id import AbstractObjectWithID


class ObjectWithIDBeanMixin(AbstractObjectWithID):
    """A bean Mixin class to automatically implement the AbstractObjectWithID specified behaviour"""

    def id(self) -> str:
        raise RuntimeError("A bean class doesn't have its own ID because it's assigned by the database, upon insert")
