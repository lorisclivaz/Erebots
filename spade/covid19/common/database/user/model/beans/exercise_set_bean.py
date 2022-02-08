from dataclasses import dataclass
from typing import List, Optional

from bson import json_util

from common.database.beans.object_with_id_bean_mixin import ObjectWithIDBeanMixin
from covid19.common.database.user.model.abstract_exercise import AbstractExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


@dataclass
class ExerciseSetBean(AbstractExerciseSet, ObjectWithIDBeanMixin):
    """A bean class to create exercise sets not directly bound to a database instance"""

    exercise_list: Optional[List[AbstractExercise]] = None
    suitable_for_goals: Optional[List[AbstractUserGoal]] = None

    def to_json_string(self) -> str:
        return json_util.dumps({
            'exercise_list': [
                exercise.to_json() for exercise in self.exercise_list
            ] if self.exercise_list else [],
            'suitable_for_goals': [
                goal.to_json() for goal in self.suitable_for_goals
            ] if self.suitable_for_goals else [],
        })
