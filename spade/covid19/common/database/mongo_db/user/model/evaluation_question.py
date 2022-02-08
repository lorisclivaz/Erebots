from __future__ import annotations  # Needed in python 3.7 to have the current class type as a return type of methods

from typing import Optional

from common.database.mongo_db.localized_object_mixin import MongoDBLocalizedObjectMixin
from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from covid19.common.database.mongo_db.models import EvaluationQuestion
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion


class MongoDBEvaluationQuestion(AbstractEvaluationQuestion, MongoDBLocalizedObjectMixin, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractEvaluationQuestion for MongoDB"""

    def __init__(self, _mongo_db_obj: EvaluationQuestion):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        MongoDBLocalizedObjectMixin.__init__(self, _mongo_db_obj)
        self._evaluation_question_mongodb_obj: EvaluationQuestion = _mongo_db_obj

    @property
    def next(self) -> Optional[MongoDBEvaluationQuestion]:
        return (
            MongoDBEvaluationQuestion(self._evaluation_question_mongodb_obj.next)
            if self._evaluation_question_mongodb_obj.next else None
        )

    @next.setter
    def next(self, new_value: Optional[AbstractEvaluationQuestion]):
        self._evaluation_question_mongodb_obj.next = EvaluationQuestion.from_json(
            new_value.to_json_string()
        ) if new_value else None
        self._evaluation_question_mongodb_obj.save()

    @property
    def previous(self) -> Optional[MongoDBEvaluationQuestion]:
        return (
            MongoDBEvaluationQuestion(self._evaluation_question_mongodb_obj.previous)
            if self._evaluation_question_mongodb_obj.previous else None
        )

    @previous.setter
    def previous(self, new_value: Optional[AbstractEvaluationQuestion]):
        self._evaluation_question_mongodb_obj.previous = EvaluationQuestion.from_json(
            new_value.to_json_string()
        ) if new_value else None
        self._evaluation_question_mongodb_obj.save()

    def to_json_string(self) -> str:
        return self._evaluation_question_mongodb_obj.to_json()

    @classmethod
    def from_json(cls, evaluation_question_json: str):
        """Creates a MongoDBEvaluationQuestion from a json string"""

        return cls(EvaluationQuestion.from_json(evaluation_question_json))
