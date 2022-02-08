from covid19.common.database.user.field_enums import DifficultyField
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion


def compute_user_level(question: AbstractEvaluationQuestion, question_answer: DifficultyField) -> str:
    """Utility method to compute the user level"""

    current_count = 1
    current_question = question

    while current_question.previous is not None:
        current_count += 1
        current_question = current_question.previous

    user_level = current_count
    current_question = question
    while current_question.next is not None:
        current_count += 1
        current_question = current_question.next

    return f"{user_level}.{question_answer.value}  /  {current_count}.{DifficultyField.EASY.value}"
