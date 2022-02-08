from dataclasses import dataclass

from bson import json_util

from covid19.common.database.user.model.abstract_chat_message import AbstractChatMessage


@dataclass
class ChatMessageBean(AbstractChatMessage):
    """A bean class to create chat message not directly bound to a database instance"""

    payload: dict

    def user_id(self) -> str:
        raise RuntimeError(
            "A bean class doesn't have its parent ID set because it's assigned by the database, upon insert"
        )

    def payload(self) -> dict:
        return self.payload

    @property
    def message_id(self) -> str:
        return self.payload.get('message_id', None)

    # It's for now only a lucky case that Telegram and CustomChat message ids are the same key string
    # Here we do not have at the moment the ability to chose the right chat platform... anyway a uniform message JSON
    # structure should be implemented as a preprocessing for incoming messages to have the certainty here
    # of the structure

    @message_id.setter
    def message_id(self, new_value: str):
        self.payload['message_id'] = new_value

    def to_json_string(self) -> str:
        return json_util.dumps(self.payload)
