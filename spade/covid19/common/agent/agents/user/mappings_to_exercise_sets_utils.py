import logging
from typing import List, TypeVar, Callable, Optional

from covid19.common.database.user.field_enums import DifficultyField, ShiftField
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)

# noinspection PyPep8Naming
T = TypeVar('T')


def on_question_and_difficulty_mapping(
        question: AbstractEvaluationQuestion,
        difficulty: DifficultyField,
        question_to_exercise_set_mappings: List[AbstractQuestionToExerciseSetMapping],
        function: Callable[[AbstractQuestionToExerciseSetMapping], T]
) -> Optional[T]:
    """Utility function to do something on a mapping identified by a question and a difficulty answer"""

    for mapping in question_to_exercise_set_mappings:
        if mapping.asked_question.id == question.id and mapping.user_answer == difficulty:
            return function(mapping)


def get_ordered_mappings_for(
        question: AbstractEvaluationQuestion,
        question_to_exercise_set_mappings: List[AbstractQuestionToExerciseSetMapping],
        reverse: bool = False
):
    """Utility method to get some question mappings in ascending ordered of difficulty"""

    question_mappings = [question_mapping
                         for question_mapping in question_to_exercise_set_mappings
                         if question_mapping.asked_question.id == question.id]
    question_mappings.sort(key=lambda question_mapping: question_mapping.user_answer.value, reverse=reverse)
    return question_mappings


def get_first_pair_with_exercise_sets(
        question: AbstractEvaluationQuestion,
        question_to_exercise_set_mappings: List[AbstractQuestionToExerciseSetMapping],
        going_towards_harder_exercises: bool
) -> (AbstractEvaluationQuestion, DifficultyField):
    """
    Utility method to get first question difficulty pair with some exercise sets,
    following the specified direction
    """

    # Since the DifficultyField enumeration goes from Impossible to Easy, we want to reverse only when we want Easy
    # as first, hence when we are NOT going towards harder exercises
    ordered_mappings = get_ordered_mappings_for(
        question,
        question_to_exercise_set_mappings,
        reverse=not going_towards_harder_exercises
    )

    for mapping in ordered_mappings:
        if mapping.suitable_exercise_sets:
            return mapping.asked_question, mapping.user_answer


def has_exercise_sets(
        question: AbstractEvaluationQuestion,
        difficulty: DifficultyField,
        question_to_exercise_set_mappings: List[AbstractQuestionToExerciseSetMapping],
):
    """Utility method to know if a question and a difficulty have some exercise sets"""

    return on_question_and_difficulty_mapping(
        question, difficulty, question_to_exercise_set_mappings,
        lambda mapping: len(mapping.suitable_exercise_sets) != 0
    )


def shift_question_or_difficulty(
        question_to_exercise_set_mappings: List[AbstractQuestionToExerciseSetMapping],
        question: AbstractEvaluationQuestion,
        difficulty: DifficultyField,
        shift_type: ShiftField
) -> (AbstractEvaluationQuestion, DifficultyField):
    """Utility method to shift the current user level"""

    logger.debug(f" Shifting from question `{question.id}` and difficulty `{difficulty}` towards `{shift_type}`")

    out_question: AbstractEvaluationQuestion = question
    out_difficulty: DifficultyField = difficulty

    if shift_type == ShiftField.NEXT:
        # Go to next difficulty level

        while out_difficulty != DifficultyField.EASY:
            # Original "difficulty response" was not easy, try to go towards it
            out_difficulty = DifficultyField(out_difficulty.value + 1)
            logger.debug(f" Original difficulty `{difficulty}`, shifted difficulty `{out_difficulty}`")

            if has_exercise_sets(question, out_difficulty, question_to_exercise_set_mappings):
                break  # New difficulty has exercises

        if difficulty == DifficultyField.EASY or (
                not has_exercise_sets(question, out_difficulty, question_to_exercise_set_mappings)
        ):
            # Original "difficulty response" was easy, or new difficulty doesn't bring exercise sets with it
            logger.debug(f" Original difficulty was EASY or {out_difficulty} has no exercises for current question")

            # Then we have to go to next question
            harder_question = question.next

            if harder_question is not None:
                logger.debug(f" Got harder question `{harder_question.id}`")

                out_question, out_difficulty = get_first_pair_with_exercise_sets(
                    harder_question, question_to_exercise_set_mappings, going_towards_harder_exercises=True
                )
                logger.debug(f" Next question level with exercises is `{out_question.id}` and `{out_difficulty}`")
            else:
                out_question = question
                out_difficulty = DifficultyField.EASY
                logger.debug(f" There's no next question. Going with `{out_question.id}` and `{out_difficulty}`")

    elif shift_type == ShiftField.PREVIOUS:
        # Go to previous level of difficulty

        while out_difficulty != DifficultyField.IMPOSSIBLE:
            # Original "difficulty response" was not impossible, try to go towards it
            out_difficulty = DifficultyField(out_difficulty.value - 1)
            logger.debug(f" Original difficulty `{difficulty}`, shifted difficulty `{out_difficulty}`")

            if has_exercise_sets(question, out_difficulty, question_to_exercise_set_mappings):
                break  # New difficulty has exercises

        if difficulty == DifficultyField.IMPOSSIBLE or (
                not has_exercise_sets(question, out_difficulty, question_to_exercise_set_mappings)
        ):
            # Original "difficulty response" was impossible, or new difficulty doesn't bring exercise sets with it
            logger.debug(
                f" Original difficulty was IMPOSSIBLE or {out_difficulty} has no exercises for current question"
            )

            # Then we have to go to previous question
            easier_question = question.previous

            if easier_question is not None:
                logger.debug(f" Got easier question `{easier_question.id}`")

                out_question, out_difficulty = get_first_pair_with_exercise_sets(
                    easier_question, question_to_exercise_set_mappings, going_towards_harder_exercises=False
                )
                logger.debug(f" Previous question level with exercises is `{out_question.id}` and `{out_difficulty}`")
            else:
                out_question = question
                out_difficulty = DifficultyField.IMPOSSIBLE
                logger.debug(f" There's no previous question. Going with `{out_question.id}` and `{out_difficulty}`")

    return out_question, out_difficulty


def get_exercise_sets_for(
        user: AbstractUser,
        question_to_exercise_set_mappings: List[AbstractQuestionToExerciseSetMapping]
) -> List[AbstractExerciseSet]:
    """Method encapsulating the logic to retrieve suitable exercise sets for a certain user level"""

    user_question = user.current_question
    user_answer = user.current_question_answer
    logger.info(f" Getting exercise sets for question `{user_question.id}` and difficulty `{user_answer}`")

    current_user_level_mapping: Optional[AbstractQuestionToExerciseSetMapping] = (
        on_question_and_difficulty_mapping(
            user_question, user_answer, question_to_exercise_set_mappings, lambda mapping: mapping
        )
    )

    suitable_exercise_sets: List[AbstractExerciseSet] = []
    if current_user_level_mapping is None:
        logger.warning(f" Not found mapping for question `{user_question.id}` and answer `{user_answer}`")
    else:
        if current_user_level_mapping.question_shift:
            logger.info(f" Current question difficulty mapping needs a shift "
                        f"`{current_user_level_mapping.question_shift}`")

            new_question, new_difficulty = shift_question_or_difficulty(
                question_to_exercise_set_mappings,
                current_user_level_mapping.asked_question,
                current_user_level_mapping.user_answer,
                current_user_level_mapping.question_shift
            )
            logger.info(f" Exercises will be taken from `{new_question.id}` and `{new_difficulty}`")

            new_level_mapping: AbstractQuestionToExerciseSetMapping = on_question_and_difficulty_mapping(
                new_question, new_difficulty, question_to_exercise_set_mappings, lambda mapping: mapping
            )
            suitable_exercise_sets = new_level_mapping.suitable_exercise_sets
        else:
            logger.info(f" Current question difficulty mapping already contains exercises, access them directly.")
            suitable_exercise_sets = current_user_level_mapping.suitable_exercise_sets

    # Filter exercise sets fitting user goals
    to_return_exercise_sets = [
        exercise_set for exercise_set in suitable_exercise_sets
        if not set([goal.id for goal in exercise_set.suitable_for_goals]).isdisjoint([goal.id for goal in user.goals])
    ]
    if not to_return_exercise_sets:
        logger.warning(f"User goals: `{[goal.text_en for goal in user.goals]}` "
                       f"does not match any of the exercises suitable goals: "
                       f"`{[[g.text_en for g in ex_set.suitable_for_goals] for ex_set in suitable_exercise_sets]}`"
                       f" Defaults sending all present exercises, even if not matching user goals")

    return to_return_exercise_sets if to_return_exercise_sets else suitable_exercise_sets
