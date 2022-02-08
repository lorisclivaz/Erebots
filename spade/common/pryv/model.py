from __future__ import annotations  # Needed in python 3.7 to have the current class type as a return type of methods

from typing import Optional, List, Any

from common.utils.enums import ValuesMixin
from common.pryv.abstract_json_response import AbstractJsonResponse


class ServiceInfo(AbstractJsonResponse):
    """Class wrapping Pryv Service info result"""

    @property
    def register(self) -> Optional[str]:
        """The URL of the register service."""
        return self.internal_json.get('register')

    @property
    def access(self) -> Optional[str]:
        """The URL to perform authentication requests."""
        return self.internal_json.get('access')

    @property
    def api(self) -> Optional[str]:
        """The API endpoint format."""
        return self.internal_json.get('api')

    @property
    def name(self) -> Optional[str]:
        """The platform name."""
        return self.internal_json.get('name')

    @property
    def home(self) -> Optional[str]:
        """The URL of the platform's home page."""
        return self.internal_json.get('home')

    @property
    def support(self) -> Optional[str]:
        """The email or URL of the support page."""
        return self.internal_json.get('support')

    @property
    def terms(self) -> Optional[str]:
        """The terms and conditions, in plain text or the URL displaying them."""
        return self.internal_json.get('terms')

    @property
    def event_types(self) -> Optional[str]:
        """The URL of the list of validated event types."""
        return self.internal_json.get('eventTypes')


class AccessLevel(ValuesMixin):
    """Enum representing possible values for access levels"""

    READ = "read"
    CONTRIBUTE = "contribute"
    MANAGE = "manage"


class DataAccessPermission(AbstractJsonResponse):
    """Class representing Pryv single data access permission"""

    @property
    def stream_id(self) -> Optional[str]:
        return self.internal_json.get('streamId')

    @stream_id.setter
    def stream_id(self, value: Optional[str]):
        self.internal_json['streamId'] = value

    @property
    def level(self) -> Optional[AccessLevel]:
        level = self.internal_json.get('level')
        return AccessLevel(level) if level else None

    @level.setter
    def level(self, value: Optional[AccessLevel]):
        self.internal_json['level'] = value.value

    @property
    def default_name(self) -> Optional[str]:
        return self.internal_json.get('defaultName')

    @default_name.setter
    def default_name(self, value: Optional[str]):
        self.internal_json['defaultName'] = value

    @classmethod
    def of(cls, stream_id: str, default_name: str, level: AccessLevel) -> DataAccessPermission:
        """Factory method for DataAccessPermission"""

        permission = cls({})
        permission.stream_id = stream_id
        permission.default_name = default_name
        permission.level = level

        return permission


class AuthStatus(ValuesMixin):
    """A class representing possible authentication statuses"""

    NEED_SIGNIN = "NEED_SIGNIN"
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"


class AuthResponse(AbstractJsonResponse):
    """A class representing the authentication API response"""

    @property
    def status(self) -> AuthStatus:
        """Authentication status"""
        status = self.internal_json.get('status', None)
        return AuthStatus(status) if status else AuthStatus.REFUSED

    @property
    def auth_url(self) -> Optional[str]:
        """The URL of the authentication page to show the user from your app as popup or webframe."""
        return self.internal_json.get('authUrl')

    @property
    def key(self) -> Optional[str]:
        """The key used to identify the auth request. It is also part of the poll URL described just below."""
        return self.internal_json.get('key')

    @property
    def poll(self) -> Optional[str]:
        """
        The poll URL to use for retrieving the auth result via an HTTP GET request.
        Responses to polling requests are the same as those from the auth request.
        """
        return self.internal_json.get('poll')

    @property
    def poll_rate_ms(self) -> Optional[int]:
        """The rate at which the poll URL can be polled, in milliseconds."""
        poll_rate_ms = self.internal_json.get('poll_rate_ms')
        return int(poll_rate_ms) if poll_rate_ms is not None else None

    @property
    def pryv_api_endpoint(self):
        """The API endpoint containing the authorization token."""
        return self.internal_json.get('apiEndpoint')

    @property
    def message(self):
        """A message indicating the reason for the failure."""
        return self.internal_json.get('message')


class PryvEvent(AbstractJsonResponse):
    """Model class to model Pryv events"""

    @property
    def id(self) -> Optional[str]:
        return self.internal_json.get('id', None)

    @property
    def stream_ids(self) -> List[str]:
        return self.internal_json.get('streamIds', [])

    @property
    def time(self) -> float:
        return self.internal_json.get('time')

    @property
    def type(self) -> str:
        return self.internal_json.get('type')

    @property
    def content(self) -> Optional[Any]:
        return self.internal_json.get('content', None)

    @property
    def attachments(self) -> Optional[List[PryvAttachment]]:
        attachments = []
        for attachment in self.internal_json.get('attachments', []):
            attachments.append(PryvAttachment(attachment))
        return attachments

    @classmethod
    def of(cls, stream_ids: List[str], content: Any, content_type: str = 'note/txt'):
        """Factory method for events"""
        return cls({'streamIds': stream_ids, 'content': content, 'type': content_type})


class PryvAttachment(AbstractJsonResponse):
    """Model class to model Pryv attachments"""

    @property
    def id(self) -> Optional[str]:
        return self.internal_json.get('id')

    @property
    def file_name(self) -> str:
        return self.internal_json.get('fileName')

    @property
    def type(self) -> str:
        return self.internal_json.get('type')

    @property
    def size(self) -> int:
        return self.internal_json.get('size')

    @property
    def read_token(self) -> str:
        return self.internal_json.get('readToken')

    @property
    def integrity(self) -> Optional[str]:
        return self.internal_json.get('integrity', None)

    @classmethod
    def of(cls, attachment_id: str, file_name: str, content_type: str, size: int, read_token: str, integrity: str = None):
        """Factory method for events"""
        return cls({'id': attachment_id, 'fileName': file_name, 'type': content_type, 'size': size,
                    'readToken': read_token, 'integrity': integrity})


class PryvStream(AbstractJsonResponse):
    """Model class to model Pryv streams"""

    @property
    def id(self) -> Optional[str]:
        return self.internal_json.get('id', None)

    @property
    def name(self) -> str:
        return self.internal_json.get('name')

    @property
    def parent_id(self) -> Optional[str]:
        return self.internal_json.get('parentId', None)

    @classmethod
    def of(cls, stream_id: str, name: str, parent_id: str = None):
        """Factory method for streams"""
        return cls({'id': stream_id, 'name': name, 'parentId': parent_id})


class AccessInfo(AbstractJsonResponse):
    """Class wrapping Pryv Access info result"""

    @property
    def permissions(self) -> Optional[List[DataAccessPermission]]:
        """
        Array of permission objects

        Ignored for personal accesses.
        If permission levels conflict (e.g. stream set to "manage" and child stream set to "contribute"),
        only the highest level is considered.
        """
        permissions_json = self.internal_json.get('permissions', [])
        return [DataAccessPermission(permission_json) for permission_json in permissions_json]

    @property
    def token(self) -> Optional[str]:
        """The token identifying the access. Automatically generated if not set when creating the access;
        slugified if necessary."""
        return self.internal_json.get('token')
