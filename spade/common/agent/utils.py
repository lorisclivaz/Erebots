from aioxmpp import jid_escape

from common.utils.dictionaries import flatten_dictionary, convert_dict_values_to_strings


def mas_message_pre_processing(to_preprocess_obj):
    """
    A function to prepare an object to be processed, in a message, by the multi agent system
    Returns a flattened and stringified dictionary of key values representing the object
    """

    flattened_object_dictionary = flatten_dictionary(dict(to_preprocess_obj))
    stringified_messaging_platform_message = convert_dict_values_to_strings(flattened_object_dictionary)
    return stringified_messaging_platform_message


def compose_user_agent_jid(user_unique_id: str, domain: str):
    """Utility function to generate the UserAgent JID, from a messaging platform message"""

    jid = f"user-{jid_escape(user_unique_id)}@{domain}"
    return jid.lower()
