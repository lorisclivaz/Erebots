from common.utils.enums import ValuesMixin


class ActionTypeField(ValuesMixin):
    """The enumeration of values that the "type" field in all Action entities can assume"""

    SEND_MESSAGE = 'send_message'
    """Send a message"""

    SEND_NOTIFICATION = 'send_notification'
    """Send a notification"""

    SEND_QUESTION = 'send_question'
    """Send a message with custom keyboard"""

    QUERY_TRANSITION = 'query_transition'
    """Query data with transition"""

    QUESTION_TRANSITION = 'question_transition'
    """Sending question with transition"""

    SIMPLE_TRANSITION = 'simple_transition'
    """Transition without user output"""


class QueryTypeField(ValuesMixin):
    """The enumeration of values that the "type" field in all Action entities can assume"""

    MSG_PER_DAY = 'msg_per_day'
    """Messages sent per day"""

    LAST_LOGIN = 'last_login'
    """Last time logged in"""

    CURRENT_WEIGHT = 'current_weight'
    """Current weight"""

    LAST_WEIGHING = 'last_weighing'
    """Last time weighing"""

    EXERCISE_TIME = 'exercise_time'
    """Daily exercise time"""

    LAST_EXERCISE = 'last_exercise'
    """Last time exercised"""

    LAST_TRACKED_MEAL = 'last_tracked_meal'
    """Last time a meal was tracked"""
