from typing import Union, Tuple, TypeVar, List, Optional

T = TypeVar('T')


def flatten_list(to_flatten_list: List[List[T]]) -> List[T]:
    """Flattens a list of lists into a flat list"""

    return [item for sublist in to_flatten_list for item in sublist]


def split_list_before_indexes(to_split: Union[List[T], Tuple], index_list: List[Optional[int]]) -> List[List[T]]:
    """Utility function to split a provided list/tuple into more lists before indexes provided in "index_list" """
    if not to_split:
        return [[]]

    if len(to_split) == 1:
        return [to_split]

    if not index_list:
        index_list = []

    return [to_split[i: j] for i, j in zip([0] + index_list, index_list + [None])]


def half_values(a_list: List[T], first_half: bool = True) -> List[T]:
    """Utility method to get half values of a list"""

    half_index = len(a_list) // 2
    if first_half:
        return a_list[:half_index]
    else:
        return a_list[half_index:]
