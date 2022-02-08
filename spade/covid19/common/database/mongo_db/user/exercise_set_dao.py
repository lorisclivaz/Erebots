import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from covid19.common.database.mongo_db.models import ExerciseSet, Exercise, UserGoal
from covid19.common.database.mongo_db.user.model.exercise_set import MongoDBExerciseSet
from covid19.common.database.user.daos import AbstractExerciseSetDAO
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet

logger = logging.getLogger(__name__)


class MongoDBExerciseSetDAO(AbstractExerciseSetDAO, MongoDBDAOMixin[MongoDBExerciseSet]):
    """Actual implementation for mongoDB of the ExerciseSet Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, ExerciseSet)

    def wrap_mongo_db_object(self, mongo_db_object: ExerciseSet) -> MongoDBExerciseSet:
        return MongoDBExerciseSet(mongo_db_object)

    def insert(self, new_exercise_set: AbstractExerciseSet) -> AbstractExerciseSet:
        to_insert_exercise_set = ExerciseSet.from_json(new_exercise_set.to_json_string())

        # NOTE: all reference fields should be "refreshed" from the string state, before inserting
        to_insert_exercise_set.exercise_list = [
            Exercise.from_json(exercise.to_json_string()) for exercise in new_exercise_set.exercise_list
        ]
        to_insert_exercise_set.suitable_for_goals = [
            UserGoal.from_json(goal.to_json_string()) for goal in new_exercise_set.suitable_for_goals
        ]

        to_insert_exercise_set.save()
        return MongoDBExerciseSet(to_insert_exercise_set)
