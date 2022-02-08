import json
from dataclasses import dataclass

from bson import json_util

from common.database.beans.localized_object_bean_mixin import LocalizedObjectBeanMixin
from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


@dataclass
class UserGoalBean(AbstractUserGoal, LocalizedObjectBeanMixin, ObjectWithIDBeanMixin):
    """A bean class to create user goals not directly bound to a database instance"""

    def to_json_string(self) -> str:
        return json_util.dumps({
            **json.loads(LocalizedObjectBeanMixin.to_json_string(self)),
        })
