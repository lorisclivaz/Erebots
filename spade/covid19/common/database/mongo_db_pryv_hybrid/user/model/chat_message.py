import logging

from bson import json_util

from common.pryv.api_wrapper import PryvAPI
from common.utils.dictionaries import remove_keys_with_none_values
from covid19.common.database.user.model.abstract_chat_message import AbstractChatMessage

logger = logging.getLogger(__name__)


class PryvChatMessage(AbstractChatMessage):
    """Actual implementation of a ChatMessage on Pryv"""

    def __init__(
            self,
            _referred_user_id: str,
            _chat_message_json_obj: dict,
            _chat_message_pryv_event_id: str,
            _pryv_api: PryvAPI,
            _user_api_endpoint_with_token: str,
    ):
        self._user_id: str = _referred_user_id
        self._chat_message_json_obj: dict = _chat_message_json_obj
        self._chat_message_pryv_event_id: str = _chat_message_pryv_event_id
        self._pryv_api = _pryv_api
        self._user_api_endpoint_with_token = _user_api_endpoint_with_token

    def _save_changes_to_event_in_pryv(self):
        """Utility function to save changes to that event in Pryv"""

        PryvAPI.save_changes_to_event(
            self._pryv_api, self._user_api_endpoint_with_token, self._chat_message_pryv_event_id,
            self._chat_message_json_obj
        )

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def message_id(self) -> str:
        return self._chat_message_json_obj.get('message_id', None)

    # It's for now only a lucky case that Telegram and CustomChat message ids are the same key string
    # Here we do not have at the moment the ability to chose the right chat platform... anyway a uniform message JSON
    # structure should be implemented as a preprocessing for incoming messages to have the certainty here
    # of the structure

    @message_id.setter
    def message_id(self, new_value: str):
        self._chat_message_json_obj['message_id'] = new_value
        self._save_changes_to_event_in_pryv()

    @property
    def payload(self) -> dict:
        return self._chat_message_json_obj

    @payload.setter
    def payload(self, new_value: dict):
        self._chat_message_json_obj = new_value
        self._save_changes_to_event_in_pryv()

    def to_json_string(self) -> str:
        return json_util.dumps(remove_keys_with_none_values(self._chat_message_json_obj))
