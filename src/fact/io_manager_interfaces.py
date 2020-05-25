# pylint: disable=too-few-public-methods
"""Interface definitions for IO Manager"""
import abc
from typing import List


class VcdElements(abc.ABC):
    """Classes to return from parser"""


class AggregatorInterface(abc.ABC):
    """Classes to return from parser"""
    @abc.abstractmethod
    def get_list(self) -> List['VcdElements']:
        """Return elements until end-of-file"""

    @abc.abstractmethod
    def namespace(self) -> str:
        """Return namespace of this aggregator"""


class EndOfFile(abc.ABC):
    """The files have finished"""
