import inspect
from typing import Optional


def add_method_to_class(function, clazz, method_name: Optional[str] = None):
    """A function to add a method to a class"""

    setattr(clazz, method_name or function.__name__, function)


def get_current_function_name() -> str:
    """Returns the current function name"""

    return inspect.stack()[1][3]


def get_caller_function_name() -> str:  # TODO 29/04/2020: maybe useful in enhancing my logging utility
    """Returns the caller function name"""

    return inspect.stack()[2][3]
