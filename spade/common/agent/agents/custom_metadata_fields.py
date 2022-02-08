from common.utils.enums import ValuesMixin


class MasMessageMetadataFields(ValuesMixin):
    """A class containing all custom MAS message metadata field names used"""

    PERFORMATIVE = "performative"
    """Used to specify a performative in a message"""

    SENDER = "sender"
    """Used to specify the sender of the message, because default sender matching not always works"""

    REQUEST_UNIQUE_CODE = "request_code"
    """Used to specify a code in requests, to receive exactly their response, using templating"""

    FAIL_MESSAGE = "fail_message"
    """Used to specify a message in case of failure"""


class MasMessagePerformatives(ValuesMixin):
    """A class containing performative legal values"""

    REQUEST = "request"
    """Performative to ask other agent some information, or to do some action"""

    INFORM = "inform"
    """Performative to communicate an information to another agent, and the information is inside the message"""

    INFORM_RESULT = "inform-result"
    """Performative to communicate a success of an action and its result inside the response"""

    FAILURE = "failure"
    """Preformative to communicate the failure of the action requested"""
