from covid19.common.xmpp_server import XMPP_SERVER_ADDRESS

TELEGRAM_GATEWAY_AGENT_NAME = "covid19_telegram_gateway_agent"
"""The Telegram gateway agent name"""

CUSTOM_CHAT_GATEWAY_AGENT_NAME = "covid19_custom_chat_gateway_agent"
"""The Custom Chat gateway agent name"""

TELEGRAM_GATEWAY_JID = f"{TELEGRAM_GATEWAY_AGENT_NAME}@{XMPP_SERVER_ADDRESS}"
"""Telegram gateway agent JID"""

CUSTOM_CHAT_GATEWAY_JID = f"{CUSTOM_CHAT_GATEWAY_AGENT_NAME}@{XMPP_SERVER_ADDRESS}"
"""Custom chat gateway agent JID"""

ALL_PLATFORMS_GATEWAY_AGENTS_JIDS = [
    CUSTOM_CHAT_GATEWAY_JID
]
"""All Gateway agents JIDs"""
