import logging
import sys
from abc import ABC, abstractmethod

from spade.behaviour import State
from spade.message import Message

from common.agent.my_logging import log, log_exception
from common.chat.message.factory import ChatMessageFactory
from common.chat.message.types import ChatMessage, ChatQuickReply, ChatActualMessage

logger = logging.getLogger(__name__)


class AbstractWaitForMessageState(State, ABC):
    """This is the main state in which we wait for the next message arrival"""

    STATE_NAME = "AbstractWaitForMessageState"
    """The name of the state which will wait next message, indefinitely (default behaviour)"""

    def __init__(self):
        super().__init__()

        self.should_set_next_state: bool = True

    async def run(self):
        msg = await self.receive(timeout=sys.maxsize)  # added max timeout to not use 100% CPU time
        if msg:
            log(self.agent, f"Message received: {msg.body}", logger, logging.DEBUG)
            try:
                await self.on_message_received(msg)
            except:
                log_exception(self.agent)

        if self.should_set_next_state:
            super().set_next_state(self.STATE_NAME)
        else:
            self.should_set_next_state = True

    def set_next_state(self, state_name):
        super().set_next_state(state_name)
        # This makes possible, to left untouched the "decision", of overriding behaviours, in next state choices
        self.should_set_next_state = False

    @abstractmethod
    async def on_message_received(self, mas_message: Message):
        """Template method called upon MAS message receiving, to handle it"""
        pass


class AbstractWaitForChatMessageState(AbstractWaitForMessageState, ABC):
    """A behaviour waiting for raw chat messages arrival, with a hook for when they arrive"""

    STATE_NAME = "AbstractWaitForChatMessageState"

    @staticmethod
    def _get_chat_message(mas_message: Message):
        """Extract the chat message from the Multi agent system message"""
        return ChatMessageFactory.from_raw_strings_dictionary(mas_message.metadata)

    async def on_message_received(self, mas_message: Message):
        await self.on_chat_message_received(mas_message, self._get_chat_message(mas_message))

    @abstractmethod
    async def on_chat_message_received(self, mas_message: Message, chat_message: ChatMessage):
        pass


class AbstractWaitForChatMessageOrQuickReplyState(AbstractWaitForChatMessageState, ABC):
    """A behaviour waiting for messages distinguishing actual message from quick replies"""

    STATE_NAME = "AbstractWaitForChatMessageOrQuickReplyState"

    async def on_chat_message_received(self, mas_message: Message, chat_message: ChatMessage):
        if await self.before_handlers(mas_message, chat_message):
            if chat_message.is_quick_reply:
                assert isinstance(chat_message, ChatQuickReply), \
                    f"{chat_message} should be a subclass of {ChatQuickReply}"
                await self.handle_quick_reply(chat_message)
            else:
                assert isinstance(chat_message, ChatActualMessage), \
                    f"{chat_message} should be a subclass of {ChatActualMessage}"
                await self.handle_message(chat_message)
        else:
            log(self.agent, "Skipping handlers because before_handlers returned False or None", logger, logging.DEBUG)

    @abstractmethod
    async def before_handlers(self, mas_message: Message, chat_message: ChatMessage) -> bool:
        pass

    @abstractmethod
    async def handle_message(self, chat_actual_message: ChatActualMessage):
        pass

    @abstractmethod
    async def handle_quick_reply(self, chat_quick_reply: ChatQuickReply):
        pass
