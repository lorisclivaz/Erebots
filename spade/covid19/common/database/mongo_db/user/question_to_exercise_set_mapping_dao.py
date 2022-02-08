import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from covid19.common.database.mongo_db.models import QuestionToExerciseSetMapping, EvaluationQuestion, ExerciseSet
from covid19.common.database.mongo_db.user.model.question_to_exercise_set_mapping import (
    MongoDBQuestionToExerciseSetMapping
)
from covid19.common.database.user.daos import AbstractQuestionToExerciseSetMappingDAO
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)

logger = logging.getLogger(__name__)


class MongoDBQuestionToExerciseSetMappingDAO(
    AbstractQuestionToExerciseSetMappingDAO, MongoDBDAOMixin[MongoDBQuestionToExerciseSetMapping]
):
    """Actual implementation for mongoDB of the QuestionToExerciseSetMapping Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, QuestionToExerciseSetMapping)

    def wrap_mongo_db_object(
            self, mongo_db_object: QuestionToExerciseSetMapping
    ) -> MongoDBQuestionToExerciseSetMapping:
        return MongoDBQuestionToExerciseSetMapping(mongo_db_object)

    def insert(
            self, new_question_to_exercise_set_mapping: AbstractQuestionToExerciseSetMapping
    ) -> AbstractQuestionToExerciseSetMapping:
        to_insert_question_to_exercise_set_mapping = QuestionToExerciseSetMapping.from_json(
            new_question_to_exercise_set_mapping.to_json_string()
        )

        # NOTE: all reference fields should be "refreshed" from the string state, before inserting
        to_insert_question_to_exercise_set_mapping.asked_question = (
            EvaluationQuestion.from_json(new_question_to_exercise_set_mapping.asked_question.to_json_string())
            if new_question_to_exercise_set_mapping.asked_question else None
        )
        to_insert_question_to_exercise_set_mapping.suitable_exercise_sets = [
            ExerciseSet.from_json(exercise_set.to_json_string())
            for exercise_set in new_question_to_exercise_set_mapping.suitable_exercise_sets
        ]

        to_insert_question_to_exercise_set_mapping.save()
        return MongoDBQuestionToExerciseSetMapping(to_insert_question_to_exercise_set_mapping)
