from mongoengine import (
    StringField, DateTimeField, BooleanField, ListField, ReferenceField, PULL, EmbeddedDocument,
    EmbeddedDocumentListField, Document, NULLIFY, CASCADE, IntField
)

from common.database.mongo_db.models import AbstractLocalizedObject, BasicUser
from covid19.common.database.enums import AgeField, SexField, WeekDayField
from covid19.common.database.user.field_enums import DifficultyField, ShiftField, FunnyField


class Exercise(AbstractLocalizedObject):
    """Model class to represent an exercise"""

    label = StringField()
    gif_path = StringField()


class UserGoal(AbstractLocalizedObject):
    """Actual model class for user goal data stored in mongo_db"""
    pass


class ExerciseSet(Document):
    """Model class to represent set of exercises"""

    exercise_list = ListField(ReferenceField(Exercise, reverse_delete_rule=PULL), default=list)
    suitable_for_goals = ListField(ReferenceField(UserGoal, reverse_delete_rule=PULL), default=list)


class EvaluationQuestion(AbstractLocalizedObject):
    """Model class to represent a question to evaluate user strength"""

    next = ReferenceField('self', reverse_delete_rule=NULLIFY)
    previous = ReferenceField('self', reverse_delete_rule=NULLIFY)


class QuestionToExerciseSetMapping(Document):
    """Model class to represent the mapping from a question (and its answer) to the related bot action"""

    asked_question = ReferenceField(EvaluationQuestion, reverse_delete_rule=CASCADE)
    user_answer = IntField(choices=DifficultyField.values(), unique_with='asked_question')
    question_shift = StringField(choices=ShiftField.values())
    suitable_exercise_sets = ListField(ReferenceField(ExerciseSet, reverse_delete_rule=PULL), default=list)


class DoneExercise(EmbeddedDocument):
    """Model class to represent a user done exercise"""

    exercise = ReferenceField(Exercise, required=True)
    ended_at = DateTimeField()
    difficulty_rating = IntField(choices=DifficultyField.values())


class SportSession(EmbeddedDocument):
    """Model class to represent user sport sessions"""

    exercise_set = ReferenceField(ExerciseSet, required=True)
    started_at = DateTimeField(required=True)
    ended_at = DateTimeField()
    aborted = BooleanField(default=False)
    done_exercises_ordered = EmbeddedDocumentListField(DoneExercise, default=list)
    fun_rating = StringField(choices=FunnyField.values())


class User(BasicUser):
    """Actual model class for user data stored in mongo_db"""

    age = StringField(choices=AgeField.values())
    sex = StringField(choices=SexField.values())
    favourite_sport_days = ListField(StringField(choices=WeekDayField.values()))
    goals = ListField(ReferenceField(UserGoal, reverse_delete_rule=PULL))
    current_question = ReferenceField(EvaluationQuestion, reverse_delete_rule=NULLIFY)
    current_question_answer = IntField(choices=DifficultyField.values())
    telegram_id = StringField()
    custom_chat_id = StringField()
    pryv_endpoint = StringField()
    registration_completed = BooleanField(default=False)
    sport_sessions = EmbeddedDocumentListField(SportSession, default=list)

    meta = {
        "strict": False,
        'ordering': ['-last_interaction']
    }


class UnreadMessage(Document):
    """Model class to represent a message directed to so some user"""

    recipient_id = StringField()
    message_json = StringField()
