from datetime import datetime
from typing import Optional, List

from common.chat.language_enum import Language
from covid19.common.database.enums import AgeField, SexField, WeekDayField
from covid19.common.database.mongo_db.user.model.evaluation_question import MongoDBEvaluationQuestion
from covid19.common.database.mongo_db.user.model.exercise import MongoDBExercise
from covid19.common.database.mongo_db.user.model.exercise_set import MongoDBExerciseSet
from covid19.common.database.mongo_db.user.model.question_to_exercise_set_mapping import (
    MongoDBQuestionToExerciseSetMapping
)
from covid19.common.database.mongo_db.user.model.unread_message import MongoDBUnreadMessage
from covid19.common.database.mongo_db.user.model.user import MongoDBUser
from covid19.common.database.mongo_db.user.model.user_goal import MongoDBUserGoal
from covid19.common.database.user.field_enums import DifficultyField, ShiftField, FunnyField
from covid19.common.database.user.model.abstract_chat_message import AbstractChatMessage
from covid19.common.database.user.model.abstract_done_exercise import AbstractDoneExercise
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_exercise import AbstractExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)
from covid19.common.database.user.model.abstract_sport_session import AbstractSportSession
from covid19.common.database.user.model.abstract_unread_message import AbstractUnreadMessage
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal
from covid19.common.database.user.model.beans.chat_message_bean import ChatMessageBean
from covid19.common.database.user.model.beans.done_exercise_bean import DoneExerciseBean
from covid19.common.database.user.model.beans.evaluation_question_bean import EvaluationQuestionBean
from covid19.common.database.user.model.beans.exercise_bean import ExerciseBean
from covid19.common.database.user.model.beans.exercise_set_bean import ExerciseSetBean
from covid19.common.database.user.model.beans.question_to_exercise_set_mapping import QuestionToExerciseSetMappingBean
from covid19.common.database.user.model.beans.sport_session_bean import SportSessionBean
from covid19.common.database.user.model.beans.unread_message_bean import UnreadMessageBean
from covid19.common.database.user.model.beans.user_bean import UserBean
from covid19.common.database.user.model.beans.user_goal_bean import UserGoalBean


class ExerciseFactory:
    """A class containing factory method for Exercises"""

    @staticmethod
    def new_exercise(
            text_en: str,
            text_it: Optional[str] = None,
            text_fr: Optional[str] = None,
            text_de: Optional[str] = None,
            label: Optional[str] = None,
            gif_path: Optional[str] = None,
    ) -> AbstractExercise:
        """A factory method to create a new Exercise"""

        return ExerciseBean(text_en, text_it, text_fr, text_de, label, gif_path)

    @staticmethod
    def from_json(exercise_json: str) -> AbstractExercise:
        """A factory method to create a Exercise from a JSON string"""

        return MongoDBExercise.from_json(exercise_json)


class UserGoalFactory:
    """A class containing factory method for UserGoals"""

    @staticmethod
    def new_user_goal(
            text_en: str,
            text_it: Optional[str] = None,
            text_fr: Optional[str] = None,
            text_de: Optional[str] = None,
    ) -> AbstractUserGoal:
        """A factory method to create a new UserGoal"""

        return UserGoalBean(text_en, text_it, text_fr, text_de)

    @staticmethod
    def from_json(user_goal_json: str) -> AbstractUserGoal:
        """A factory method to create a UserGoal from a JSON string"""

        return MongoDBUserGoal.from_json(user_goal_json)


class ExerciseSetFactory:
    """A class containing factory method for ExerciseSets"""

    @staticmethod
    def new_exercise_set(
            exercise_list: List[AbstractExercise] = None,
            suitable_for_goals: List[AbstractUserGoal] = None,
    ) -> AbstractExerciseSet:
        """A factory method to create a new ExerciseSet"""

        if exercise_list is None:
            exercise_list = []
        if suitable_for_goals is None:
            suitable_for_goals = []

        return ExerciseSetBean(exercise_list, suitable_for_goals)

    @staticmethod
    def from_json(exercise_set_json: str) -> AbstractExerciseSet:
        """A factory method to create an ExerciseSet from a JSON string"""

        return MongoDBExerciseSet.from_json(exercise_set_json)


class EvaluationQuestionFactory:
    """A class containing factory method for EvaluationQuestions"""

    @staticmethod
    def new_evaluation_question(
            text_en: str,
            text_it: Optional[str] = None,
            text_fr: Optional[str] = None,
            text_de: Optional[str] = None,
            next_question: Optional[AbstractEvaluationQuestion] = None,
            previous_question: Optional[AbstractEvaluationQuestion] = None,
    ) -> AbstractEvaluationQuestion:
        """A factory method to create a new EvaluationQuestion"""

        return EvaluationQuestionBean(text_en, text_it, text_fr, text_de, next_question, previous_question)

    @staticmethod
    def from_json(evaluation_question_json: str) -> AbstractEvaluationQuestion:
        """A factory method to create an EvaluationQuestion from a JSON string"""

        return MongoDBEvaluationQuestion.from_json(evaluation_question_json)


class QuestionToExerciseSetMappingFactory:
    """A class containing factory method for QuestionToExerciseSetMappings"""

    @staticmethod
    def new_question_to_exercise_set_mapping(
            asked_question: Optional[AbstractEvaluationQuestion] = None,
            user_answer: Optional[DifficultyField] = None,
            question_shift: Optional[ShiftField] = None,
            suitable_exercise_sets: List[AbstractExerciseSet] = None,
    ) -> AbstractQuestionToExerciseSetMapping:
        """A factory method to create a new QuestionToExerciseSetMapping"""

        if suitable_exercise_sets is None:
            suitable_exercise_sets = []

        return QuestionToExerciseSetMappingBean(asked_question, user_answer, question_shift, suitable_exercise_sets)

    @staticmethod
    def from_json(question_to_exercise_set_mapping_json: str) -> AbstractQuestionToExerciseSetMapping:
        """A factory method to create an QuestionToExerciseSetMapping from a JSON string"""

        return MongoDBQuestionToExerciseSetMapping.from_json(question_to_exercise_set_mapping_json)


class DoneExerciseFactory:
    """A class containing factory methods for DoneExercise"""

    @staticmethod
    def new_done_exercise(
            exercise: AbstractExercise,
            ended_at: Optional[datetime] = None,
            difficulty_rating: Optional[DifficultyField] = None,
    ) -> AbstractDoneExercise:
        """A factory method to create a new DoneExercise"""

        return DoneExerciseBean(
            exercise=exercise,
            ended_at=ended_at,
            difficulty_rating=difficulty_rating,
        )


class SportSessionFactory:
    """A class containing factory methods for SportSession"""

    @staticmethod
    def new_sport_session(
            exercise_set: AbstractExerciseSet,
            started_at: datetime = None,
            ended_at: Optional[datetime] = None,
            aborted: bool = False,
            done_exercises_ordered: List[AbstractDoneExercise] = None,
            fun_rating: Optional[FunnyField] = None,
    ) -> AbstractSportSession:
        """A factory method to create a new SportSession"""

        if started_at is None:
            started_at = datetime.now()
        if done_exercises_ordered is None:
            done_exercises_ordered = []

        return SportSessionBean(
            exercise_set=exercise_set,
            started_at=started_at,
            ended_at=ended_at,
            aborted=aborted,
            done_exercises_ordered=done_exercises_ordered,
            fun_rating=fun_rating,
        )


class CustomChatMessageFactory:
    """A class containing factory methods for ChatMessage"""

    @staticmethod
    def new_chat_message(payload: dict, ) -> AbstractChatMessage:
        """A factory method to create a new ChatMessage"""

        return ChatMessageBean(payload=payload)


class UnreadMessageFactory:
    """A class containing factory method for UnreadMessage"""

    @staticmethod
    def new_unread_message(recipient_id: str, message_json: dict) -> AbstractUnreadMessage:
        """A factory method to create a new UnreadMessage"""

        return UnreadMessageBean(recipient_id, message_json)

    @staticmethod
    def from_json(unread_message_json: str) -> AbstractUnreadMessage:
        """A factory method to create an UnreadMessage from a JSON string"""

        return MongoDBUnreadMessage.from_json(unread_message_json)


class UserFactory:
    """A class containing factory methods for Users"""

    @staticmethod
    def new_user(
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            language: Optional[Language] = None,
            last_interaction: datetime = datetime.min,
            age: Optional[AgeField] = None,
            sex: Optional[SexField] = None,
            favourite_sport_days: List[WeekDayField] = None,
            goals: List[AbstractUserGoal] = None,
            current_question: Optional[AbstractEvaluationQuestion] = None,
            current_question_answer: Optional[DifficultyField] = None,
            telegram_id: Optional[str] = None,
            custom_chat_id: Optional[str] = None,
            pryv_endpoint: Optional[str] = None,
            registration_completed: bool = False,
            sport_sessions: List[AbstractSportSession] = None,
    ) -> AbstractUser:
        """A factory method to create a new User"""

        if favourite_sport_days is None:
            favourite_sport_days = []
        if goals is None:
            goals = []
        if sport_sessions is None:
            sport_sessions = []

        return UserBean(first_name, last_name, language, last_interaction, age, sex, favourite_sport_days, goals,
                        current_question, current_question_answer, telegram_id, custom_chat_id, pryv_endpoint,
                        registration_completed, sport_sessions)

    @staticmethod
    def from_json(user_json: str) -> AbstractUser:
        """A factory method to create a User from a JSON string"""

        return MongoDBUser.from_json(user_json)
