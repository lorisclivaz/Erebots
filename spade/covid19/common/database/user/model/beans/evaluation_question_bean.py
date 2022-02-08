import json
from dataclasses import dataclass
from typing import Optional

from bson import json_util

from common.database.beans.localized_object_bean_mixin import LocalizedObjectBeanMixin
from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion


@dataclass
class EvaluationQuestionBean(AbstractEvaluationQuestion, LocalizedObjectBeanMixin, ObjectWithIDBeanMixin):
    """A bean class to create an evaluation question not directly bound to a database instance"""

    next: Optional[AbstractEvaluationQuestion] = None
    previous: Optional[AbstractEvaluationQuestion] = None

    def to_json_string(self) -> str:
        return json_util.dumps({
            **json.loads(LocalizedObjectBeanMixin.to_json_string(self)),
            'next': self.next.to_json() if self.next else None,
            'previous': self.previous.to_json() if self.previous else None,
        })
