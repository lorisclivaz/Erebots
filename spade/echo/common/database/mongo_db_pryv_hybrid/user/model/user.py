import base64
import json
import sys
import logging
from typing import Optional, List, MutableMapping

from bson import json_util

from common.chat.language_enum import Language
from common.database.mongo_db.object_with_id_mixin import MongoDBObjectWithIDMixin
from common.database.mongo_db.user.user_mixin import MongoDBUserMixin
from common.pryv.api_wrapper import PryvAPI
from common.pryv.model import PryvEvent, PryvAttachment
from common.utils.dictionaries import remove_keys_with_none_values
from echo.common.database.mongo_db_pryv_hybrid.models import User, PryvStoredData
from echo.common.database.mongo_db_pryv_hybrid.user.model.chat_message import PryvChatMessage
from echo.common.database.user.model.abstract_chat_message import AbstractChatMessage
from echo.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class MongoDBAndPryvUser(AbstractUser, MongoDBUserMixin, MongoDBObjectWithIDMixin):
    """Actual implementation of AbstractUser for MongoDB and Pryv hybrid"""

    def __init__(
            self,
            _mongo_db_obj: User,
            _pryv_server_domain: str
    ):
        MongoDBObjectWithIDMixin.__init__(self, _mongo_db_obj)
        MongoDBUserMixin.__init__(self, _mongo_db_obj)
        self._user_mongodb_obj: User = _mongo_db_obj
        self._pryv_api = PryvAPI(_pryv_server_domain)

        self._chat_message_id_to_pryv_event_id: MutableMapping[str, str] = {}

    def _access_pryv_stream_events_of(self, stream_id: str, sort_ascending: bool = True, limit: int = sys.maxsize / 2
                                      ) -> List[PryvEvent]:
        """Utility method to access all the events in a Pryv stream"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            return self._pryv_api.get_events(
                user_endpoint_with_token, streams=[stream_id], sort_ascending=sort_ascending, limit=limit
            )
        else:
            return []

    def _access_pryv_last_value_of(self, stream_id: str) -> Optional[str]:
        """Utility method to access the last value of a Pryv stream"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            stream_events = self._pryv_api.get_events(user_endpoint_with_token, streams=[stream_id], limit=1)
            return stream_events[0].content if stream_events else None
        else:
            return None

    def _set_pryv_new_value_for(self, stream_id: str, new_value: str, content_type: str = 'note/txt') -> Optional[
        PryvEvent]:
        """Utility method to set a new event in a Pryv stream"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            return self._pryv_api.create_event(user_endpoint_with_token, [stream_id], new_value,
                                               content_type=content_type)
        else:
            logger.warning(f"Not setting value {new_value} for {stream_id},"
                           f" because the user has not a Pryv endpoint set.")

    def _add_attachment_for(self, event_id: str, data) -> Optional[PryvEvent]:
        """Utility method to set a new event in a Pryv stream"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            return self._pryv_api.add_attachment(user_endpoint_with_token, event_id, data)
        else:
            logger.warning(f"Not adding attachment {data} to event {event_id},"
                           f" because the user has not a Pryv endpoint set.")

    def _get_attachment_of(self, event_id: str, attachment_id: str, read_token: str) -> Optional[PryvAttachment]:
        """Utility method to retrieven an attachment of a Pryv event"""
        user_endpoint_with_token = self._user_mongodb_obj.pryv_endpoint
        if user_endpoint_with_token:
            return self._pryv_api.get_attachment(user_endpoint_with_token, event_id, attachment_id, read_token)
        else:
            logger.warning(f"Not retrieving attachment {attachment_id} of event {event_id},"
                           f" because the user has not a Pryv endpoint set.")

    @property
    def first_name(self) -> Optional[str]:
        first_name = self._access_pryv_last_value_of(PryvStoredData.FIRST_NAME.value[0])
        return first_name

    @first_name.setter
    def first_name(self, new_value: str):
        self._set_pryv_new_value_for(PryvStoredData.FIRST_NAME.value[0], new_value)

    # last_name is not here because not saved on pryv currently

    @property
    def language(self) -> Optional[Language]:
        language = self._access_pryv_last_value_of(PryvStoredData.LANGUAGE.value[0])
        return Language(language) if language else None

    @language.setter
    def language(self, new_value: Language):
        self._set_pryv_new_value_for(PryvStoredData.LANGUAGE.value[0], new_value.value)

    @property
    def telegram_id(self) -> Optional[str]:
        return self._user_mongodb_obj.telegram_id

    @telegram_id.setter
    def telegram_id(self, new_value: str):
        self._user_mongodb_obj.telegram_id = new_value
        self._user_mongodb_obj.save()

    @property
    def custom_chat_id(self) -> Optional[str]:
        return self._user_mongodb_obj.custom_chat_id

    @custom_chat_id.setter
    def custom_chat_id(self, new_value: str):
        self._user_mongodb_obj.custom_chat_id = new_value
        self._user_mongodb_obj.save()

    @property
    def pryv_endpoint(self) -> Optional[str]:
        return self._user_mongodb_obj.pryv_endpoint

    @pryv_endpoint.setter
    def pryv_endpoint(self, new_value: str):
        self._user_mongodb_obj.pryv_endpoint = new_value
        self._user_mongodb_obj.save()

    @property
    def registration_completed(self) -> bool:
        return self._user_mongodb_obj.registration_completed

    @registration_completed.setter
    def registration_completed(self, new_value: bool):
        self._user_mongodb_obj.registration_completed = new_value
        self._user_mongodb_obj.save()

    @property
    def chat_messages(self) -> List[AbstractChatMessage]:
        chat_message_events = self._access_pryv_stream_events_of(PryvStoredData.CHAT_MESSAGES.value[0])
        result_messages = []
        self._chat_message_id_to_pryv_event_id = {}
        for chat_message_event in chat_message_events:
            chat_message = PryvChatMessage(
                self.id, json_util.loads(chat_message_event.content), chat_message_event.id, self._pryv_api,
                self._user_mongodb_obj.pryv_endpoint
            )
            result_messages.append(chat_message)
            self._chat_message_id_to_pryv_event_id[chat_message.message_id] = chat_message_event.id

        return result_messages

    def append_chat_message(self, new_value: AbstractChatMessage):
        created_event = self._set_pryv_new_value_for(
            PryvStoredData.CHAT_MESSAGES.value[0],
            json_util.dumps(remove_keys_with_none_values(dict(new_value.to_json())))
        )

        if created_event:
            self._chat_message_id_to_pryv_event_id[new_value.message_id] = created_event.id

    def replace_chat_message(self, message_id: str, new_value: AbstractChatMessage):
        pryv_event_id = self._chat_message_id_to_pryv_event_id[message_id]
        PryvAPI.save_changes_to_event(
            self._pryv_api, self._user_mongodb_obj.pryv_endpoint, pryv_event_id,
            new_value.payload
        )

    def delete_chat_message(self, message_id: str):
        pryv_event_id = self._chat_message_id_to_pryv_event_id[message_id]
        self._pryv_api.delete_event(self._user_mongodb_obj.pryv_endpoint, pryv_event_id)

    def to_json_string(self) -> str:
        mongo_db_json = json.loads(self._user_mongodb_obj.to_json())

        first_name = self.first_name
        last_name = self.last_name
        language = self.language

        hybrid_json = {
            **mongo_db_json,
            'first_name': first_name,
            'last_name': last_name,
            'language': language.value if language else None,
        }
        return json_util.dumps(remove_keys_with_none_values(hybrid_json))

    @property
    def chat_images(self) -> List[AbstractChatMessage]:
        # TODO: Implement retrieving all images sent by the user. This method will be used during data analysis as a
        #  first step of retrieving images per user
        raise NotImplementedError

    def append_chat_image(self, new_value: AbstractChatMessage):
        image_event = self._set_pryv_new_value_for(
            PryvStoredData.CHAT_IMAGES.value[0],
            json_util.dumps(remove_keys_with_none_values(dict(new_value.to_json()))),
            content_type='picture/attached'
        )

        attachment_event = self._add_attachment_for(
            image_event.id, base64.urlsafe_b64decode(new_value.payload.get('photo'))
        )
        # TODO: Fix this part after the Pryv instance has been updated
        if attachment_event and len(attachment_event.attachments) > 0:
            for attachment in attachment_event.attachments:
                test2 = self._get_attachment_of(
                    attachment_event.id, attachment_event.attachments[0].id, attachment_event.attachments[0].read_token
                )

                image_url = (
                    f"{self._pryv_api.extract_user_api(self._user_mongodb_obj.pryv_endpoint)}events/{image_event.id}/"
                    f"{attachment['id']}"
                    f"?readToken={attachment['readToken']}"
                )
                new_value.payload['text'] = image_url
                self.append_chat_message(new_value)
