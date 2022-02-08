import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from covid19.common.database.mongo_db.models import Exercise
from covid19.common.database.mongo_db.user.model.exercise import MongoDBExercise
from covid19.common.database.user.daos import AbstractExerciseDAO
from covid19.common.database.user.model.abstract_exercise import AbstractExercise

logger = logging.getLogger(__name__)


class MongoDBExerciseDAO(AbstractExerciseDAO, MongoDBDAOMixin[MongoDBExercise]):
    """Actual implementation for mongoDB of the Exercise Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, Exercise)

    def wrap_mongo_db_object(self, mongo_db_object: Exercise) -> MongoDBExercise:
        return MongoDBExercise(mongo_db_object)

    def insert(self, new_exercise: AbstractExercise) -> AbstractExercise:
        to_insert_exercise = Exercise.from_json(new_exercise.to_json_string())
        to_insert_exercise.save()
        return MongoDBExercise(to_insert_exercise)
