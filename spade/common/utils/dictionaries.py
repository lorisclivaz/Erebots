import collections
from typing import TypeVar, Mapping, Any

T1 = TypeVar('T1')
T2 = TypeVar('T2')


def flatten_dictionary(to_flatten_dictionary, keys_separator='_', _parent_key='') -> dict:
    """Flattens a dictionary, joining nested keys"""

    items = []
    for k, v in to_flatten_dictionary.items():
        new_key = _parent_key + keys_separator + k if _parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dictionary(v, keys_separator=keys_separator, _parent_key=new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def convert_dict_values_to_strings(dictionary: Mapping[T1, Any]) -> Mapping[T1, str]:
    """Utility function to convert dictionary values to strings"""

    return {k: f"{str(v)}" for (k, v) in dictionary.items()}


def inverse_dictionary(dictionary: Mapping[T1, T2]) -> Mapping[T2, T1]:
    """Utility function to get the inverse mapping on a dictionary"""

    return {v: k for k, v in dictionary.items()}


def remove_keys_with_none_values(dictionary):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # For Python 3, write `list(d.items())`; `d.items()` won’t work
    # For Python 2, write `d.items()`; `d.iteritems()` won’t work
    for key, value in list(dictionary.items()):
        if value is None:
            del dictionary[key]
        elif isinstance(value, dict):
            remove_keys_with_none_values(value)
    return dictionary  # For convenience
