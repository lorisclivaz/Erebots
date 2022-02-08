from abc import ABC

from common.database.abstract_dao import AbstractDAO
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_exercise import AbstractExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)
from covid19.common.database.user.model.abstract_unread_message import AbstractUnreadMessage
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal


class AbstractExerciseDAO(AbstractDAO[AbstractExercise], ABC):
    """A base class to implement Data Access Object for Exercise"""
    pass


class AbstractUserGoalDAO(AbstractDAO[AbstractUserGoal], ABC):
    """A base class to implement Data Access Object for UserGoal"""
    pass


class AbstractExerciseSetDAO(AbstractDAO[AbstractExerciseSet], ABC):
    """A base class to implement Data Access Object for ExerciseSet"""
    pass


class AbstractEvaluationQuestionDAO(AbstractDAO[AbstractEvaluationQuestion], ABC):
    """A base class to implement Data Access Object for EvaluationQuestion"""
    pass


class AbstractQuestionToExerciseSetMappingDAO(AbstractDAO[AbstractQuestionToExerciseSetMapping], ABC):
    """A base class to implement Data Access Object for QuestionToExerciseSetMapping"""
    pass


class AbstractUserDAO(AbstractDAO[AbstractUser], ABC):
    """A base class to implement Data Access Object for User"""
    pass


class AbstractUnreadMessageDAO(AbstractDAO[AbstractUnreadMessage], ABC):
    """A base class to implement Data Access Object for UnreadMessage"""
    pass
