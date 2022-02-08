from typing import List

from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from covid19.common.database.mongo_db.models import ExerciseSet, Exercise, UserGoal
from covid19.common.database.mongo_db.user.model.exercise import MongoDBExercise
from covid19.common.database.mongo_db.user.model.user_goal import MongoDBUserGoal
from covid19.common.database.user.model.abstract_exercise import AbstractExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


class MongoDBExerciseSet(AbstractExerciseSet, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractExerciseSet for MongoDB"""

    def __init__(self, _mongo_db_obj: ExerciseSet):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        self._exercise_set_mongodb_obj: ExerciseSet = _mongo_db_obj

    @property
    def exercise_list(self) -> List[MongoDBExercise]:
        exercise_list = self._exercise_set_mongodb_obj.exercise_list
        return [MongoDBExercise(exercise) for exercise in exercise_list] if exercise_list else []

    @exercise_list.setter
    def exercise_list(self, new_values: List[AbstractExercise]):
        self._exercise_set_mongodb_obj.exercise_list = [
            Exercise.from_json(new_value.to_json_string()) for new_value in new_values
        ]
        self._exercise_set_mongodb_obj.save()

    @property
    def suitable_for_goals(self) -> List[MongoDBUserGoal]:
        suitable_for_goals = self._exercise_set_mongodb_obj.suitable_for_goals
        return [MongoDBUserGoal(goal) for goal in suitable_for_goals] if suitable_for_goals else []

    @suitable_for_goals.setter
    def suitable_for_goals(self, new_values: List[AbstractUserGoal]):
        self._exercise_set_mongodb_obj.suitable_for_goals = [
            UserGoal.from_json(new_value.to_json_string()) for new_value in new_values
        ]
        self._exercise_set_mongodb_obj.save()

    def to_json_string(self) -> str:
        return self._exercise_set_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, exercise_set_json: str):
        """Creates a MongoDBExerciseSet from a json string"""

        return cls(ExerciseSet.from_json(exercise_set_json))
