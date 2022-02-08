import json
import logging
import os
import uuid
from pathlib import Path
from typing import Optional, List, Tuple, Callable

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_request import Request, FileField
from aiohttp.web_response import Response
from bson import json_util

from common.agent.web.controllers import (
    create_json_response, OBJECT_ID_URL_MATCHER_STRING, CORS_HEADER, get_request_time_window
)
from common.agent.web.mime_type_utils import get_mime_type_from_extension
from common.database.abstract_dao import AbstractDAO, T
from common.pryv.api_wrapper import PryvAPI
from common.pryv.model import PryvEvent
from covid19.common.agent.agents.level_model import compute_user_level
from covid19.common.database.mongo_db_pryv_hybrid.models import PryvStoredData
from covid19.common.database.user.daos import (
    AbstractExerciseDAO, AbstractExerciseSetDAO, AbstractUserGoalDAO, AbstractQuestionToExerciseSetMappingDAO,
    AbstractEvaluationQuestionDAO, AbstractUserDAO
)
from covid19.common.database.user.factory import (
    ExerciseFactory, ExerciseSetFactory, QuestionToExerciseSetMappingFactory, EvaluationQuestionFactory, UserGoalFactory
)
from covid19.common.database.user.field_enums import DifficultyField, ShiftField
from covid19.common.database.user.model.abstract_evaluation_question import AbstractEvaluationQuestion
from covid19.common.database.user.model.abstract_exercise import AbstractExercise
from covid19.common.database.user.model.abstract_exercise_set import AbstractExerciseSet
from covid19.common.database.user.model.abstract_question_to_exercise_set_mapping import (
    AbstractQuestionToExerciseSetMapping
)
from covid19.common.database.user.model.abstract_user import AbstractUser
from covid19.common.database.user.model.abstract_user_goal import AbstractUserGoal

logger = logging.getLogger(__name__)

API_MOUNT_POINT = "/api/v1"


def _get_form_field(form_data, form_field: str) -> Optional[str]:
    """Utility function to get form data from client"""

    return form_data.get(form_field) if form_data.get(form_field) else None


def create_exercise_gif_controller(exercises_dao: AbstractExerciseDAO):
    """Creates the coroutine handling the getting of the GIF image about an exercise"""

    async def exercise_gif_controller(request: Request):
        """The controller handling exercise GIF request"""

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request GIF of object with ID: `{object_id}`")

        an_object: Optional[AbstractExercise] = exercises_dao.find_by_id(object_id)
        if an_object and an_object.gif_path:
            file_path = Path(os.path.join(Path(__file__), GO_UP_PATH_STRING, an_object.gif_path))
            norm_path = os.path.normpath(file_path)
            with open(norm_path, "rb") as file:
                return Response(body=file.read(), content_type=get_mime_type_from_extension(norm_path))
        else:
            raise HTTPNotFound(reason=f"No GIF for object with ID `{object_id}`", headers=CORS_HEADER)

    return exercise_gif_controller


def create_exercise_controller(exercises_dao: AbstractExerciseDAO):
    """Creates the coroutine handling the creation of objects"""

    async def exercise_controller(request: Request):
        """The controller handling exercise creation request"""

        form_data = await request.post()

        new_exercise = ExerciseFactory.new_exercise(
            text_en=_get_form_field(form_data, 'text_en'),
            text_it=_get_form_field(form_data, 'text_it'),
            text_fr=_get_form_field(form_data, 'text_fr'),
            text_de=_get_form_field(form_data, 'text_de'),
            label=_get_form_field(form_data, 'label'),
            gif_path=_get_gif_file(form_data)
        )

        inserted_obj = exercises_dao.insert(new_exercise)
        return await create_json_response(inserted_obj.to_json_string())

    return exercise_controller


def create_modify_exercise_controller(exercises_dao: AbstractExerciseDAO):
    """Creates the coroutine handling the modification of objects"""

    async def exercise_modification_controller(request: Request):
        """The controller handling exercise modification request"""

        form_data = await request.post()

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request to modify object with ID: `{object_id}` "
                     f"with following receive data: {str(list(form_data.items()))}")

        an_object: Optional[AbstractExercise] = exercises_dao.find_by_id(object_id)
        if an_object:
            an_object.text_en = _get_form_field(form_data, 'text_en')
            an_object.text_it = _get_form_field(form_data, 'text_it')
            an_object.text_fr = _get_form_field(form_data, 'text_fr')
            an_object.text_de = _get_form_field(form_data, 'text_de')
            an_object.label = _get_form_field(form_data, 'label')

            gif_path = _get_gif_file(form_data)
            if gif_path:
                _remove_old_gif_file(an_object.gif_path)
                an_object.gif_path = gif_path

            return await create_json_response(an_object.to_json_string())
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return exercise_modification_controller


def create_delete_object_controller(
        dao: AbstractDAO[T],
        on_before_object_deletion: Callable[[T], None] = lambda x: None
):
    """Creates the coroutine handling the deletion of objects"""

    async def object_deletion_controller(request: Request):
        """The controller handling object deletion request"""

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request to delete object with ID: `{object_id}`")

        an_object: Optional[T] = dao.find_by_id(object_id)
        if an_object:
            on_before_object_deletion(an_object)
            dao.delete_by_id(object_id)
            return Response(body='{}', headers=CORS_HEADER)
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return object_deletion_controller


def create_delete_exercise_controller(exercises_dao: AbstractExerciseDAO):
    """Creates the coroutine handling the deletion of objects"""

    return create_delete_object_controller(exercises_dao, lambda exercise: _remove_old_gif_file(exercise.gif_path))


def _load_list_form_field_with_dao(form_data, form_id_field_name: str, dao: AbstractDAO[T]) -> List[T]:
    """Utility function to load a list field inside form data, with provided dao"""

    ids_list = json.loads(form_data.get(form_id_field_name))
    return [dao.find_by_id(an_id) for an_id in ids_list]


def create_exercise_set_controller(
        exercise_sets_dao: AbstractExerciseSetDAO,
        exercises_dao: AbstractExerciseDAO,
        user_goals_dao: AbstractUserGoalDAO
):
    """Creates the coroutine handling the creation of objects"""

    async def exercise_set_controller(request: Request):
        """The controller handling exercise set creation request"""

        form_data = await request.post()

        exercises = _load_list_form_field_with_dao(form_data, 'exercise_list', exercises_dao)
        suitable_goals = _load_list_form_field_with_dao(form_data, 'suitable_for_goals', user_goals_dao)

        new_exercise_set = ExerciseSetFactory.new_exercise_set(
            exercise_list=exercises,
            suitable_for_goals=suitable_goals
        )

        inserted_obj = exercise_sets_dao.insert(new_exercise_set)
        return await create_json_response(inserted_obj.to_json_string())

    return exercise_set_controller


def create_modify_exercise_set_controller(
        exercise_sets_dao: AbstractExerciseSetDAO,
        exercises_dao: AbstractExerciseDAO,
        user_goals_dao: AbstractUserGoalDAO
):
    """Creates the coroutine handling the modification of objects"""

    async def exercise_set_modification_controller(request: Request):
        """The controller handling exercise set modification request"""

        form_data = await request.post()

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request to modify object with ID: `{object_id}` "
                     f"with following receive data: {str(list(form_data.items()))}")

        an_object: Optional[AbstractExerciseSet] = exercise_sets_dao.find_by_id(object_id)
        if an_object:
            an_object.exercise_list = _load_list_form_field_with_dao(form_data, 'exercise_list', exercises_dao)
            an_object.suitable_for_goals = _load_list_form_field_with_dao(form_data, 'suitable_for_goals',
                                                                          user_goals_dao)

            return await create_json_response(an_object.to_json_string())
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return exercise_set_modification_controller


def _load_exercise_set_mapping_data(
        form_data,
        questions_dao: AbstractEvaluationQuestionDAO,
        exercise_sets_dao: AbstractExerciseSetDAO,
) -> Tuple[AbstractEvaluationQuestion, DifficultyField, List[AbstractExerciseSet], ShiftField]:
    """Function refactoring the loading logic for data received to create or modify exercise set mappings"""

    question = questions_dao.find_by_id(_get_form_field(form_data, 'asked_question'))
    answer = DifficultyField(int(_get_form_field(form_data, 'user_answer')))

    exercise_sets = None
    question_shift = None
    if not form_data.get('suitable_exercise_sets') or form_data.get('suitable_exercise_sets') == '[]':
        question_shift = ShiftField(_get_form_field(form_data, 'question_shift'))
    else:
        exercise_sets = _load_list_form_field_with_dao(form_data, 'suitable_exercise_sets', exercise_sets_dao)

    return question, answer, exercise_sets, question_shift


def create_exercise_set_mapping_controller(
        question_to_exercise_sets_dao: AbstractQuestionToExerciseSetMappingDAO,
        exercise_sets_dao: AbstractExerciseSetDAO,
        questions_dao: AbstractEvaluationQuestionDAO,
):
    """Creates the coroutine handling the creation of objects"""

    async def exercise_set_mapping_controller(request: Request):
        """The controller handling exercise set mapping creation request"""

        form_data = await request.post()

        question, answer, exercise_sets, question_shift = _load_exercise_set_mapping_data(
            form_data, questions_dao, exercise_sets_dao
        )

        new_exercise_set_mapping = QuestionToExerciseSetMappingFactory.new_question_to_exercise_set_mapping(
            question, answer, question_shift, exercise_sets
        )

        inserted_obj = question_to_exercise_sets_dao.insert(new_exercise_set_mapping)
        return await create_json_response(inserted_obj.to_json_string())

    return exercise_set_mapping_controller


def create_modify_exercise_set_mapping_controller(
        question_to_exercise_sets_dao: AbstractQuestionToExerciseSetMappingDAO,
        exercise_sets_dao: AbstractExerciseSetDAO,
        questions_dao: AbstractEvaluationQuestionDAO,
):
    """Creates the coroutine handling the modification of objects"""

    async def exercise_set_mapping_modification_controller(request: Request):
        """The controller handling exercise set mapping modification request"""

        form_data = await request.post()

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request to modify object with ID: `{object_id}` "
                     f"with following receive data: {str(list(form_data.items()))}")

        question, answer, exercise_sets, question_shift = _load_exercise_set_mapping_data(
            form_data, questions_dao, exercise_sets_dao
        )

        an_object: Optional[AbstractQuestionToExerciseSetMapping] = question_to_exercise_sets_dao.find_by_id(object_id)
        if an_object:
            an_object.asked_question = question
            an_object.user_answer = answer
            an_object.suitable_exercise_sets = exercise_sets
            an_object.question_shift = question_shift

            return await create_json_response(an_object.to_json_string())
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return exercise_set_mapping_modification_controller


def create_question_controller(questions_dao: AbstractEvaluationQuestionDAO):
    """Creates the coroutine handling the creation of objects"""

    async def question_controller(request: Request):
        """The controller handling question creation request"""

        form_data = await request.post()

        current_last_question: AbstractEvaluationQuestion = list(questions_dao.find_by(next=None).values())[0]

        new_question = EvaluationQuestionFactory.new_evaluation_question(
            text_en=_get_form_field(form_data, 'text_en'),
            text_it=_get_form_field(form_data, 'text_it'),
            text_fr=_get_form_field(form_data, 'text_fr'),
            text_de=_get_form_field(form_data, 'text_de'),
            previous_question=current_last_question
        )

        inserted_obj = questions_dao.insert(new_question)
        current_last_question.next = inserted_obj

        return await create_json_response(inserted_obj.to_json_string())

    return question_controller


def create_modify_question_controller(questions_dao: AbstractEvaluationQuestionDAO):
    """Creates the coroutine handling the modification of objects"""

    async def question_modification_controller(request: Request):
        """The controller handling question modification request"""

        form_data = await request.post()

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request to modify object with ID: `{object_id}` "
                     f"with following receive data: {str(list(form_data.items()))}")

        an_object: Optional[AbstractEvaluationQuestion] = questions_dao.find_by_id(object_id)
        if an_object:
            an_object.text_en = _get_form_field(form_data, 'text_en')
            an_object.text_it = _get_form_field(form_data, 'text_it')
            an_object.text_fr = _get_form_field(form_data, 'text_fr')
            an_object.text_de = _get_form_field(form_data, 'text_de')

            previous_question_id = _get_form_field(form_data, 'previous')
            next_question_id = _get_form_field(form_data, 'next')

            previous_question = questions_dao.find_by_id(previous_question_id) if previous_question_id else None
            next_question = questions_dao.find_by_id(next_question_id) if next_question_id else None

            an_object.previous = previous_question
            an_object.next = next_question

            return await create_json_response(an_object.to_json_string())
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return question_modification_controller


def create_delete_question_controller(questions_dao: AbstractEvaluationQuestionDAO):
    """Creates the coroutine handling the deletion of objects"""

    def question_deletion_callback(to_be_deleted_question: AbstractEvaluationQuestion):
        """Callback called when a question is about to be deleted"""

        previous_question = to_be_deleted_question.previous
        next_question = to_be_deleted_question.next

        if previous_question:
            previous_question.next = next_question

        if next_question:
            next_question.previous = previous_question

    return create_delete_object_controller(questions_dao, question_deletion_callback)


def create_user_goal_controller(user_goal_dao: AbstractUserGoalDAO):
    """Creates the coroutine handling the creation of objects"""

    async def user_goal_controller(request: Request):
        """The controller handling user goal creation request"""

        form_data = await request.post()

        new_user_goal = UserGoalFactory.new_user_goal(
            text_en=_get_form_field(form_data, 'text_en'),
            text_it=_get_form_field(form_data, 'text_it'),
            text_fr=_get_form_field(form_data, 'text_fr'),
            text_de=_get_form_field(form_data, 'text_de'),
        )

        inserted_obj = user_goal_dao.insert(new_user_goal)
        return await create_json_response(inserted_obj.to_json_string())

    return user_goal_controller


def create_modify_user_goal_controller(user_goal_dao: AbstractUserGoalDAO):
    """Creates the coroutine handling the modification of objects"""

    async def user_goal_modification_controller(request: Request):
        """The controller handling user goal modification request"""

        form_data = await request.post()

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request to modify object with ID: `{object_id}` "
                     f"with following receive data: {str(list(form_data.items()))}")

        an_object: Optional[AbstractUserGoal] = user_goal_dao.find_by_id(object_id)
        if an_object:
            an_object.text_en = _get_form_field(form_data, 'text_en')
            an_object.text_it = _get_form_field(form_data, 'text_it')
            an_object.text_fr = _get_form_field(form_data, 'text_fr')
            an_object.text_de = _get_form_field(form_data, 'text_de')

            return await create_json_response(an_object.to_json_string())
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return user_goal_modification_controller


def create_user_level_history_controller(
        user_dao: AbstractUserDAO,
        questions_dao: AbstractEvaluationQuestionDAO,
        pryv_api: PryvAPI
):
    """Creates the coroutine handling the retrieval of user level history"""

    async def user_level_history_controller(request: Request):
        """The controller handling user level history retrieval"""

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request for data about user with ID: `{object_id}`")

        a_user: Optional[AbstractUser] = user_dao.find_by_id(object_id)
        if a_user:
            start_timestamp, end_timestamp = await get_request_time_window(request)

            def get_pryv_events_for(stream_id: str) -> List[PryvEvent]:
                return pryv_api.get_events(
                    a_user.pryv_endpoint,
                    from_timestamp=start_timestamp / 1000.0,
                    to_timestamp=end_timestamp / 1000.0,
                    streams=[stream_id],
                    sort_ascending=True
                )

            questions_history = get_pryv_events_for(PryvStoredData.CURRENT_QUESTION.value[0])
            question_answers_history = get_pryv_events_for(PryvStoredData.CURRENT_QUESTION_ANSWER.value[0])

            if len(questions_history) != len(question_answers_history):
                logger.warning(
                    f" Mismatch! The retrieved questions count is different from the questions-answer count!"
                )
                # Here we could make a cleanup of data, checking whether the events are near in time

            question_answer_pair_history = zip(
                [(question.content, question.time) for question in questions_history],
                [(answer.content, answer.time) for answer in question_answers_history]
            )
            result_for_client = []
            for ((question_content, question_time), (answer_content, answer_time)) in question_answer_pair_history:
                question_id = json_util.loads(question_content)
                question = questions_dao.find_by_id(question_id)
                answer = DifficultyField(int(answer_content))
                result_for_client.append(
                    {
                        'timestamp': question_time,
                        'level': compute_user_level(question, answer).split('/')[0].strip()
                    }
                )

            return await create_json_response(result_for_client)
        else:
            raise HTTPNotFound(reason=f"No user with ID `{object_id}`", headers=CORS_HEADER)

    return user_level_history_controller


EXERCISE_GIF_ASSETS_FOLDER = "covid19/assets/gif/"

GO_UP_PATH_STRING = '../../../../../../'


def _save_and_get_gif_project_relative_path(
        form_data_image_file: FileField,
        image_file_name: str = None
) -> str:
    """Utility function to save image file coming from the web client"""

    if image_file_name is None:
        image_file_name = uuid.uuid4()

    exercise_gif_path = f'{EXERCISE_GIF_ASSETS_FOLDER}{image_file_name}.gif'
    destination_file_path = os.path.normpath(Path(os.path.join(Path(__file__), GO_UP_PATH_STRING, exercise_gif_path)))

    with open(destination_file_path, 'wb') as destination_file:
        destination_file.write(form_data_image_file.file.read())

    return exercise_gif_path


def _get_gif_file(form_data) -> Optional[str]:
    """Refactoring of the code to save and get the gif path to be stored into DB, if present in POST request"""

    if form_data.get('gif-file'):
        file_field: FileField = form_data.get('gif-file')
        return _save_and_get_gif_project_relative_path(file_field)
    else:
        return None


def _remove_old_gif_file(gif_path: Optional[str]):
    """Utility method to remove old GIF files after updating a GIF"""

    if gif_path:
        try:
            os.remove(gif_path)
            logger.info(f"Deleted {gif_path}")
        except:
            logger.warning(f"Could not delete file {gif_path}, which is no more useful")
