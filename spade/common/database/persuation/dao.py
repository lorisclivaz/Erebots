from abc import ABC

from common.database.abstract_dao import AbstractDAO
from common.database.persuation.model.abstract_strategy import AbstractStrategy


class AbstractStrategyDAO(AbstractDAO[AbstractStrategy], ABC):
    """A base class to implement Data Access Object for Strategy"""
    pass
