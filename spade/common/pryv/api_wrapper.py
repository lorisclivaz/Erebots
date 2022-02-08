from __future__ import annotations  # Needed in python 3.7 to have the current class type as a return type of methods

import logging
import sys
from typing import List, Optional, Any, Mapping

import requests
from bson import json_util

from common.pryv.server_domain import PRYV_PROJECT_ID, PRYV_PROJECT_NAME
from common.utils.dictionaries import remove_keys_with_none_values
from common.pryv.model import (
    ServiceInfo, DataAccessPermission, AuthResponse, AuthStatus, PryvEvent, PryvStream, AccessInfo, PryvAttachment
)
from echo.common.database.mongo_db_pryv_hybrid.models import PryvStoredData

logger = logging.getLogger(__name__)


class PryvAPI:
    """A class wrapping Pryv API calls"""

    SERVICE_INFO_ENDPOINT = "/service/info"

    def __init__(self, domain: str):
        self.domain = domain
        self.register_inferred_url = f"https://reg.{domain}"

    @property
    def service_info(self) -> ServiceInfo:
        """Retrieves service info from Pryv domain"""

        to_fetch_url = f"{self.register_inferred_url}{self.SERVICE_INFO_ENDPOINT}"
        logger.info(f" Getting service_info at `{to_fetch_url}`")

        return ServiceInfo(requests.get(to_fetch_url).json())

    def request_auth(
            self,
            requesting_app_id: str,
            requested_permissions: List[DataAccessPermission],
            language_code: Optional[str] = None,
            return_url: Optional[str] = None
    ) -> AuthResponse:
        """Requests for app authorization"""

        access_url = self.service_info.access
        logger.info(f" Doing request_auth, using access url: `{access_url}`")
        response = requests.post(access_url, json={
            'requestingAppId': requesting_app_id,
            'requestedPermissions': [
                permission.to_json() for permission in requested_permissions
            ],
            'languageCode': language_code,
            'returnURL': return_url
        })
        logger.debug(f" request_auth() response: `{str(response.json())}`")
        return AuthResponse(response.json())

    @staticmethod
    def fetch_poll_url(previous_auth_response: AuthResponse) -> AuthResponse:
        """Fetches the poll url of the AuthResponse if sign-in was needed"""

        if previous_auth_response.status == AuthStatus.ACCEPTED:
            logger.info(f" Auth accepted. {previous_auth_response.to_json_string()}")
            return previous_auth_response
        elif previous_auth_response.status == AuthStatus.REFUSED:
            logger.info(f" Auth refused. {previous_auth_response.to_json_string()}")
            return previous_auth_response
        else:
            poll_url = previous_auth_response.poll
            logger.info(f" Doing polling at: `{poll_url}`")
            return AuthResponse(requests.get(poll_url).json())

    @staticmethod
    def extract_user_api(user_api_endpoint_with_token: str) -> str:
        """Utility method to extract api endpoint from the url with token"""
        return 'https://' + user_api_endpoint_with_token.split('@')[1]

    @staticmethod
    def extract_user_username(user_api_endpoint_with_token: str) -> str:
        """Utility method to extract user username from the url with token"""
        return user_api_endpoint_with_token.split('@')[1].split('.')[0].lower()

    @staticmethod
    def extract_user_token(user_api_endpoint_with_token: str) -> str:
        """Utility method to extract api endpoint from the url with token"""
        return user_api_endpoint_with_token.split('@')[0].replace('https://', '')

    def get_events(
            self,
            user_api_endpoint_with_token: str,
            from_timestamp: Optional[float] = None,
            to_timestamp: Optional[float] = None,
            streams: Optional[List[str]] = None,
            sort_ascending: Optional[bool] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = sys.maxsize / 2,
    ) -> List[PryvEvent]:
        """Get events from Pryv API"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Could not query Pryv!! Provided user API endpoint is None")
            return []

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}events"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )

        params = {}
        if from_timestamp is not None:
            params['fromTime'] = from_timestamp
        if to_timestamp is not None:
            params['toTime'] = to_timestamp
        if streams is not None:
            params['streams'] = streams
        if sort_ascending is not None:
            params['sortAscending'] = sort_ascending
        if skip is not None:
            params['skip'] = skip
        if limit is not None:
            params['limit'] = limit

        logger.debug(f" Retrieving events at: {actual_endpoint} with params {str(params)}")
        response = requests.get(actual_endpoint, params)
        logger.debug(f" Response: {response.json()}")
        return [PryvEvent(event) for event in response.json().get('events', [])]

    def create_event(
            self,
            user_api_endpoint_with_token: str,
            stream_ids: List[str],
            content: Any,
            content_type: str = 'note/txt'
    ) -> Optional[PryvEvent]:
        """Create an event for the provided stream"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Not creating event!! Provided user API endpoint is None")
            return None

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}events"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )

        logger.info(f" Creating event at: {actual_endpoint}")
        response = requests.post(actual_endpoint, json=PryvEvent.of(
            stream_ids=stream_ids,
            content=content,
            content_type=content_type
        ).to_json())

        if response.status_code == 201:
            return PryvEvent(response.json().get('event'))
        else:
            logger.error(f" Error creating event: [{response.status_code}] {str(response.json())}")
            return None

    def update_event(
            self,
            user_api_endpoint_with_token: str,
            to_modify_event_id: str,
            new_event_fields: Mapping
    ) -> Optional[PryvEvent]:
        """Update an event for the provided stream"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Not updating event!! Provided user API endpoint is None")
            return None

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}events/{to_modify_event_id}"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )

        logger.info(f" Updating event at: {actual_endpoint}")
        response = requests.put(actual_endpoint, json=new_event_fields)

        if response.status_code == 200:
            return PryvEvent(response.json().get('event'))
        else:
            logger.error(f" Error updating event: [{response.status_code}] {str(response.json())}")
            return None

    def delete_event(
            self,
            user_api_endpoint_with_token: str,
            to_delete_event_id: str
    ) -> Optional[PryvEvent]:
        """Trash/Delete an event for the provided stream"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Not deleting event!! Provided user API endpoint is None")
            return None

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}events/{to_delete_event_id}"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )

        logger.info(f" Deleting event at: {actual_endpoint}")
        response = requests.delete(actual_endpoint)

        if response.status_code == 200:
            deleted_event = response.json().get('event', None)
            return PryvEvent(deleted_event) if deleted_event is not None else None
        else:
            logger.error(f" Error deleting event: [{response.status_code}] {str(response.json())}")
            return None

    def add_attachment(
            self,
            user_api_endpoint_with_token: str,
            event_id: str,
            attachment: Any,
    ) -> Optional[PryvEvent]:
        """Add an attachment to the provided event"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Not adding attachment!! Provided user API endpoint is None")
            return None

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}events/{event_id}"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )

        logger.info(f" Adding attachment to event: {actual_endpoint}")
        response = requests.post(actual_endpoint, files={'file': ('test.jpg', attachment, 'image/jpg')})

        if response.status_code == 200:
            return PryvEvent(response.json().get('event'))
        else:
            logger.error(f" Error adding attachment: [{response.status_code}] {str(response.json())}")
            return None

    def get_attachment(
            self,
            user_api_endpoint_with_token: str,
            event_id: str,
            attachment_id: str,
            read_token: str
    ) -> Optional[PryvAttachment]:
        """Retrieve an attachment for the provided event"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Not retrieving attachment!! Provided user API endpoint is None")
            return None

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}events/{event_id}/{attachment_id}/image.jpg"
            f"?readToken={read_token}"
        )

        logger.info(f" Retrieving attachment of event: {actual_endpoint}")
        response = requests.get(
            actual_endpoint, headers={"Authorization": self.extract_user_token(user_api_endpoint_with_token)}
        )

        if response.status_code == 200:
            return PryvAttachment(response.json().get('attachment'))
        else:
            logger.error(f" Error retrieving attachment: [{response.status_code}] {str(response.json())}")
            return None

    def check_stream_presence(
            self,
            user_api_endpoint_with_token: str,
            to_find_stream_id: str
    ) -> Optional[PryvStream]:
        """Gets stream info, returns None in case the stream is not present"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Couldn't check stream presence!! Provided user API endpoint is None")
            return None

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}streams"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )

        response = requests.get(actual_endpoint)
        retrieved_streams = [PryvStream(stream) for stream in response.json().get('streams', [])]

        for stream in retrieved_streams:
            if stream.id == to_find_stream_id:
                return stream

        return None

    def create_stream(
            self,
            user_api_endpoint_with_token: str,
            stream_id: str,
            name: str,
            parent_id: str = None
    ) -> Optional[PryvStream]:
        """Create a stream if not already present"""

        if user_api_endpoint_with_token is None:
            logger.warning(f" Not creating stream!! Provided user API endpoint is None")
            return None

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}streams"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )

        logger.info(f" Creating stream at: {actual_endpoint}")
        response = requests.post(actual_endpoint, json=PryvStream.of(
            stream_id=stream_id,
            name=name,
            parent_id=parent_id
        ).to_json())

        if response.status_code == 201:
            logger.info(f" Successfully created stream: [id: {stream_id}, name: {name}]")
            return PryvStream(response.json().get('stream'))
        else:
            logger.error(f" Error creating stream: [{response.status_code}] {str(response.json())}")
            return None

    def get_access_info(
            self,
            user_api_endpoint_with_token: str,
    ) -> Optional[AccessInfo]:
        """Gets access info about the provided token"""

        actual_endpoint = (
            f"{self.extract_user_api(user_api_endpoint_with_token)}access-info"
            f"?auth={self.extract_user_token(user_api_endpoint_with_token)}"
        )
        response = requests.get(actual_endpoint)

        if response.status_code == 200:
            json_response = response.json()
            if json_response.get('error', None) is None:
                return AccessInfo(response.json())
        else:
            logger.exception(f"Pryv access info failed: {response.status_code}")

        return None

    @staticmethod
    def save_changes_to_event(pryv_api: PryvAPI, api_endpoint: str, event_id: str, new_json_object: dict):
        """Saves changes to provided event on Pryv"""

        pryv_api.update_event(
            api_endpoint,
            event_id,
            {'content': json_util.dumps(remove_keys_with_none_values(new_json_object))}
        )

    def create_stream_structure(self, user_api_endpoint_with_token: str):
        """Creates the initial stream structure of the application"""

        self.create_stream(user_api_endpoint_with_token, PRYV_PROJECT_ID, PRYV_PROJECT_NAME)

        for value in PryvStoredData.values():
            self.create_stream(user_api_endpoint_with_token, value[0], value[1], PRYV_PROJECT_ID)
