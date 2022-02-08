import logging

from common.database.mongo_db.dao_mixin import MongoDBDAOMixin
from covid19.common.database.mongo_db.models import EvaluationQuestion
from covid19.common.database.mongo_db.user.model.evaluation_question import MongoDBEvaluationQuestion
from covid19.common.database.user.daos import AbstractEvaluationQuestionDAO
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion

logger = logging.getLogger(__name__)


class MongoDBEvaluationQuestionDAO(AbstractEvaluationQuestionDAO, MongoDBDAOMixin[MongoDBEvaluationQuestion]):
    """Actual implementation for mongoDB of the EvaluationQuestion Data Access Object"""

    def __init__(self):
        MongoDBDAOMixin.__init__(self, EvaluationQuestion)

    def wrap_mongo_db_object(self, mongo_db_object: EvaluationQuestion) -> MongoDBEvaluationQuestion:
        return MongoDBEvaluationQuestion(mongo_db_object)

    def insert(self, new_evaluation_question: AbstractEvaluationQuestion) -> AbstractEvaluationQuestion:
        to_insert_evaluation_question = EvaluationQuestion.from_json(new_evaluation_question.to_json_string())

        # NOTE: all reference fields should be "refreshed" from the string state, before inserting
        to_insert_evaluation_question.next = (
            EvaluationQuestion.from_json(new_evaluation_question.next.to_json_string())
            if new_evaluation_question.next else None
        )
        to_insert_evaluation_question.previous = (
            EvaluationQuestion.from_json(new_evaluation_question.previous.to_json_string())
            if new_evaluation_question.previous else None
        )

        to_insert_evaluation_question.save()
        return MongoDBEvaluationQuestion(to_insert_evaluation_question)
