from typing import Optional

from common.database.mongo_db.localized_object_mixin import MongoDBLocalizedObjectMixin
from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from covid19.common.database.mongo_db.models import Exercise
from covid19.common.database.user.model.abstract_exercise import AbstractExercise


class MongoDBExercise(AbstractExercise, MongoDBLocalizedObjectMixin, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractExercise for MongoDB"""

    def __init__(self, _mongo_db_obj: Exercise):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        MongoDBLocalizedObjectMixin.__init__(self, _mongo_db_obj)
        self._exercise_mongodb_obj: Exercise = _mongo_db_obj

    @property
    def label(self) -> Optional[str]:
        return self._exercise_mongodb_obj.label

    @label.setter
    def label(self, new_value: str):
        self._exercise_mongodb_obj.label = new_value
        self._exercise_mongodb_obj.save()

    @property
    def gif_path(self) -> Optional[str]:
        return self._exercise_mongodb_obj.gif_path

    @gif_path.setter
    def gif_path(self, new_value: str):
        self._exercise_mongodb_obj.gif_path = new_value
        self._exercise_mongodb_obj.save()

    def to_json_string(self) -> str:
        return self._exercise_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, exercise_json: str):
        """Creates a MongoDBExercise from a json string"""

        return cls(Exercise.from_json(exercise_json))
