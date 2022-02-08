import asyncio
import logging
from datetime import datetime, timedelta
from threading import Timer
from typing import Optional

from aiohttp.web_exceptions import (
    HTTPBadRequest, HTTPInternalServerError, HTTPUnauthorized, HTTPNotFound
)
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from common.agent.web.controllers import create_json_response, CORS_HEADER, OBJECT_ID_URL_MATCHER_STRING
from common.chat.language_enum import Language
from common.custom_chat.client_notification_manager import ClientNotificationManager
from common.pryv.api_wrapper import PryvAPI
from common.pryv.model import DataAccessPermission, AuthStatus, AuthResponse
from covid19.common.database.mongo_db_pryv_hybrid.models import PryvStoredData
from covid19.common.database.user.daos import AbstractUserDAO
from covid19.common.database.user.factory import UserFactory
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


def create_get_status_controller():
    """Creates the coroutine handling app status checking"""

    status_json_field_name = "status"
    status_online_value = "online"

    async def status_controller(_request: Request):
        """The controller handling status request"""

        return await create_json_response({
            status_json_field_name: status_online_value
        })

    return status_controller


def create_app_login_controller(user_dao: AbstractUserDAO, pryv_api_wrapper: PryvAPI):
    """Creates the coroutine handling the app login call"""

    pryv_requesting_app_id = 'covid19-physio-project'

    language_code_query_field = "lang"
    default_language = "en"

    max_polling_duration = timedelta(days=1)
    """Duration after which not authorized logins polling timers, are cancelled"""

    async def app_login_controller(request: Request):
        """The controller handling app login request"""

        logger.info(f" Start Pryv registration process...")

        language_code = request.query.get(language_code_query_field, default_language)

        auth_response = pryv_api_wrapper.request_auth(
            requesting_app_id=pryv_requesting_app_id,
            requested_permissions=[
                DataAccessPermission.of(info[0], info[1], info[2])
                for info in PryvStoredData.values()
            ],
            language_code=language_code
        )

        await _start_polling_for_access_granting(
            user_dao, pryv_api_wrapper, auth_response, max_age=datetime.now() + max_polling_duration
        )

        return await create_json_response(auth_response.to_json_string())

    return app_login_controller


async def _start_polling_for_access_granting(
        user_dao: AbstractUserDAO, pryv_api_wrapper: PryvAPI, auth_response: AuthResponse, max_age: datetime,
):
    """Function to poll the Pryv api to verify if the user granted access authorization"""

    next_auth_response = pryv_api_wrapper.fetch_poll_url(auth_response)
    if next_auth_response.status == AuthStatus.ACCEPTED:
        logger.info(f" User gave Pryv access to our Bot.")

        pryv_endpoint_url = next_auth_response.pryv_api_endpoint
        user_username = PryvAPI.extract_user_username(pryv_endpoint_url)

        users_with_username = list(user_dao.find_by(custom_chat_id=user_username).values())
        if len(users_with_username) > 1:
            raise Exception(f"More than 1 user with custom_chat_id = `{user_username}`")

        already_present_user = users_with_username[0] if len(users_with_username) == 1 else None
        if already_present_user is None:
            # New user should be created
            new_user = UserFactory.new_user(pryv_endpoint=pryv_endpoint_url, custom_chat_id=user_username)
            user_dao.insert(new_user)
            logger.info(f" New user added: {new_user.pryv_endpoint}")
        else:
            # Present user should be updated
            logger.info(
                f" Update pryv endpoint from `{already_present_user.pryv_endpoint}` to `{pryv_endpoint_url}` ..."
            )
            already_present_user.pryv_endpoint = pryv_endpoint_url

    elif next_auth_response.status == AuthStatus.REFUSED:
        logger.info(f" User refused to give Pryv access.")

    elif next_auth_response.status == AuthStatus.NEED_SIGNIN:
        logger.info(f" Not accepted yet...")
        if datetime.now() > max_age:
            logger.info(f" Auth request with url {auth_response.poll} went on prescription. Will not poll this again.")
        else:
            Timer(
                next_auth_response.poll_rate_ms / 1000,
                asyncio.gather,
                [_start_polling_for_access_granting(user_dao, pryv_api_wrapper, next_auth_response, max_age)],
                {'loop': asyncio.get_running_loop()}
            ).start()
    else:
        logger.error(f" Unknown auth response status: {next_auth_response.status}")


def create_credentials_checker_controller(user_dao: AbstractUserDAO, pryv_api_wrapper: PryvAPI):
    """Creates the coroutine handling the credentials check"""

    user_id_query_field = "userId"

    async def credential_check_controller(request: Request):
        """The controller handling credential check request"""

        to_check_user_id = request.query.get(user_id_query_field, "")

        if to_check_user_id == "":
            raise HTTPBadRequest(reason="Malformed user id query", headers=CORS_HEADER)

        logger.info(f" Checking credentials for {to_check_user_id}...")

        users_with_id = list(user_dao.find_by(custom_chat_id=to_check_user_id).values())
        if len(users_with_id) > 1:
            raise HTTPInternalServerError(
                reason=f"More than 1 user with custom_chat_id = `{to_check_user_id}`",
                headers=CORS_HEADER
            )

        already_present_user = users_with_id[0] if len(users_with_id) == 1 else None

        # A new login is needed if the user is None or its endpoint is None
        new_login_needed = already_present_user is None or already_present_user.pryv_endpoint is None

        # If the user is present and endpoint is present, check for latter validity
        if not new_login_needed:
            logger.info(f" User was present and had a Pryv endpoint. Check for token validity...")
            pryv_access_info = pryv_api_wrapper.get_access_info(already_present_user.pryv_endpoint)
            if pryv_access_info is None:
                # Token revoked or something wrong with the user permissions, request Pryv auth again
                logger.info(f" User Pryv token invalid. New login needed...")
                new_login_needed = True

        if new_login_needed:
            raise HTTPUnauthorized(
                reason="User token expired or token revoked by user. New login is needed.",
                headers=CORS_HEADER
            )
        else:
            logger.info(f" `{to_check_user_id}` Pryv token still valid.")
            return await create_json_response({})

    return credential_check_controller


def _get_one_user_by_id_or_error(user_id: str, user_dao: AbstractUserDAO):
    """Checks if user id is present, raising error in other cases"""
    if user_id == "":
        raise HTTPBadRequest(reason="Malformed user id query", headers=CORS_HEADER)

    users_with_id = list(user_dao.find_by(custom_chat_id=user_id).values())
    if len(users_with_id) > 1:
        raise HTTPInternalServerError(reason=f"More than 1 user with custom_chat_id = `{user_id}`", headers=CORS_HEADER)
    elif len(users_with_id) == 0:
        raise HTTPNotFound(reason=f"User with custom_chat_id = `{user_id}` not found", headers=CORS_HEADER)

    return users_with_id[0]


def create_message_sender_info_controller(user_dao: AbstractUserDAO):
    """Creates the coroutine handling the message sender info retrieval"""

    user_id_query_field = "userId"

    server_user_id_json_field = "serverUserId"
    first_name_json_field = "firstName"
    language_json_field = "language"

    async def message_sender_controller(request: Request):
        """The controller handling message sender info request"""

        to_retrieve_user_id = request.query.get(user_id_query_field, "")

        the_user = _get_one_user_by_id_or_error(to_retrieve_user_id, user_dao)

        user_info_obj = {
            user_id_query_field: to_retrieve_user_id,
            server_user_id_json_field: the_user.id,
            first_name_json_field: the_user.first_name,
            language_json_field: Language.to_ietf_tag(the_user.language),
        }
        logger.info(f" Sending `{to_retrieve_user_id}` info object: {str(user_info_obj)}")
        return await create_json_response(user_info_obj)

    return message_sender_controller


def create_user_messages_controller(user_dao: AbstractUserDAO):
    """Creates the coroutine handling the user messages retrieval"""

    user_id_query_field = "userId"

    messages_json_field = "messages"

    async def user_messages_controller(request: Request):
        """The controller handling user messages request"""

        messages_of_user_id = request.query.get(user_id_query_field, "")

        the_user = _get_one_user_by_id_or_error(messages_of_user_id, user_dao)

        user_messages_obj = {messages_json_field: [message.to_json() for message in the_user.chat_messages]}
        logger.info(f" Sending `{messages_of_user_id}` messages. Count: {len(user_messages_obj[messages_json_field])}")
        return await create_json_response(
            user_messages_obj,
            custom_headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        )

    return user_messages_controller


def create_user_language_controller(user_dao: AbstractUserDAO):
    """Creates the coroutine handling the user language modification"""

    language_code_payload_key = "languageCode"

    async def user_language_controller(request: Request):
        """The controller handling user language changes request"""

        form_data = await request.post()

        object_id = request.match_info[OBJECT_ID_URL_MATCHER_STRING]
        logger.debug(f" Request of changing language to user with ID: `{object_id}`")

        an_object: Optional[AbstractUser] = user_dao.find_by_id(object_id)
        if an_object:
            ietf_language_code = form_data.get(language_code_payload_key, None)
            if ietf_language_code:
                an_object.language = Language.from_ietf_tag(ietf_language_code)
                logger.info(f" Language changed to `{ietf_language_code}`.")
                return await create_json_response({})
            else:
                raise HTTPBadRequest(reason="Form data not present or not correctly formatted.", headers=CORS_HEADER)
        else:
            raise HTTPNotFound(reason=f"No object with ID `{object_id}`", headers=CORS_HEADER)

    return user_language_controller


def create_webapp_serving_controller(web_app_index_file: str):
    """Create the controller serving the web application"""

    async def webapp_serving_controller(_: Request):
        """Server the web application one page"""

        return Response(body=f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="UTF-8">
              <title>Chat</title>
            </head>
            <body>
            <iframe 
              src="{web_app_index_file}" 
              style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;">
                Your browser doesn't support iframes
            </iframe>
            </body>
            </html>
        """, headers=CORS_HEADER, content_type="text/html")

    return webapp_serving_controller


def create_user_unread_messages_controller(user_dao: AbstractUserDAO, notification_manager: ClientNotificationManager):
    """Creates the coroutine handling the user unread messages retrieval"""

    user_id_query_field = "userId"

    messages_json_field = "messages"

    async def user_unread_messages_controller(request: Request):
        """The controller handling user unread messages request"""

        messages_of_user_id = request.query.get(user_id_query_field, "")

        _get_one_user_by_id_or_error(messages_of_user_id, user_dao)  # Left here for error raising purposes

        unread_messages_obj = {messages_json_field: notification_manager.get_messages(messages_of_user_id)}
        logger.info(f" `{messages_of_user_id}` unread messages count: {len(unread_messages_obj[messages_json_field])}")
        return await create_json_response(
            unread_messages_obj,
            custom_headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        )

    return user_unread_messages_controller
