import json
from dataclasses import dataclass
from typing import Optional

from bson import json_util

from common.database.beans.localized_object_bean_mixin import LocalizedObjectBeanMixin
from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from covid19.common.database.user.model.abstract_exercise import AbstractExercise


@dataclass
class ExerciseBean(AbstractExercise, LocalizedObjectBeanMixin, ObjectWithIDBeanMixin):
    """A bean class to create exercises not directly bound to a database instance"""

    label: Optional[str] = None
    gif_path: Optional[str] = None

    def to_json_string(self) -> str:
        return json_util.dumps({
            **json.loads(LocalizedObjectBeanMixin.to_json_string(self)),
            'label': self.label,
            'gif_path': self.gif_path,
        })
