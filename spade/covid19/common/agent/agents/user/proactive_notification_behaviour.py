import datetime
import logging
from typing import List, Optional

import emoji
from spade.behaviour import TimeoutBehaviour, OneShotBehaviour

from common.agent.agents.abstract_user_agent import AbstractUserAgent
from common.agent.agents.interaction_texts import localize
from common.agent.my_logging import log
from common.chat.platform.abstract_messaging_platform import AbstractMessagingPlatform
from common.chat.platform.types import ChatPlatform
from common.custom_chat.chat.message_content_factory import CustomChatMessageContentFactory
from common.custom_chat.client_notification_manager import ClientNotificationManager
from covid19.common.agent.agents.interaction_texts import HEY_YOU_SHOULD_EXERCISE
from covid19.common.database.user.model.abstract_user import AbstractUser

logger = logging.getLogger(__name__)


class ProactiveNotificationSettingBehaviour(OneShotBehaviour):
    """A behaviour to set the proactive notification behaviour"""

    def __init__(self, notification_hours: List[int], user: Optional[AbstractUser],
                 client_notification_manager: Optional[ClientNotificationManager]):
        super().__init__()
        self._notification_hours = notification_hours
        self._user = user
        self._client_notification_manager = client_notification_manager

    async def run(self):
        timedelta_till_next_exercise = self._compute_next_hour_timedelta(self._notification_hours)
        notification_datetime = (
                datetime.datetime.now() + timedelta_till_next_exercise
        )
        if notification_datetime < datetime.datetime.now():
            # Check to make sure the notification date is not past, otherwise notify immediately
            notification_datetime = datetime.datetime.now() + datetime.timedelta(minutes=1)

        self.agent.add_behaviour(ProactiveNotificationBehaviour(
            start_at=notification_datetime,
            notification_hours=self._notification_hours,
            user=self._user,
            client_notification_manager=self._client_notification_manager
        ))

        log(self.agent, f"Exercise notification will be dispatched at `{str(notification_datetime)}`", logger)

    @staticmethod
    def _compute_next_hour_timedelta(hour_list: List[int]) -> Optional[datetime.timedelta]:
        """Utility method to compute the current timedelta towards the nearest hour, w.r.t. provided hour list"""
        if not hour_list:
            return None
        else:
            hour = datetime.datetime.now().hour + 1
            delta_hours = 1
            while hour not in hour_list:
                hour = (hour + 1) % 24
                delta_hours += 1
            return datetime.timedelta(hours=delta_hours)


class ProactiveNotificationBehaviour(TimeoutBehaviour):
    """A behaviour to send a proactive notification to the user"""

    DEFAULT_NOTIFICATION_PLATFORM = ChatPlatform.CUSTOM_CHAT

    @staticmethod
    def _select_user_platform_id(user: AbstractUser):
        """Internal strategy to select the user id related to messaging platform where to send the notification"""
        return user.custom_chat_id

    def __init__(self, start_at, notification_hours: List[int], user: Optional[AbstractUser],
                 client_notification_manager: Optional[ClientNotificationManager]):
        super().__init__(start_at)
        self._notification_hours = notification_hours
        self._user = user
        self._client_notification_manager = client_notification_manager

    async def run(self):
        agent: AbstractUserAgent = self.agent
        messaging_platform: AbstractMessagingPlatform = (
            agent.messaging_platforms.get(self.DEFAULT_NOTIFICATION_PLATFORM, None)
        )
        if messaging_platform is None:
            log(self.agent,
                f"Could not send proactive notification because of missing messaging platform "
                f"({self.DEFAULT_NOTIFICATION_PLATFORM.value})."
                f" Will start sending messages after the user communication to the backend through this platform.",
                logger)
        elif self._user is None:
            log(self.agent,
                f"Could not send proactive notification because of missing user instance."
                f" Will start sending messages after the user communication to the backend.",
                logger)
        elif self._client_notification_manager is None:
            log(self.agent,
                f"Could not send proactive notification because of missing client notification manager instance.",
                logger, logging.WARNING)
        else:
            log(self.agent, f"Enqueuing proactive notification to be fetched...", logger)
            language = self._user.language
            localized_text = localize(HEY_YOU_SHOULD_EXERCISE, language)
            self._client_notification_manager.add_message(
                self._select_user_platform_id(self._user),
                CustomChatMessageContentFactory.create_message_content(emoji.emojize(localized_text))
            )
            log(self.agent, f"Notification enqueued.", logger)

        # Anyway re add the scheduling behaviour to wait for next time a proactive notification should be sent
        agent.add_behaviour(ProactiveNotificationSettingBehaviour(
            self._notification_hours, self._user, self._client_notification_manager
        ))
