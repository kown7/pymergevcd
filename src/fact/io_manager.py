"""Manage input"""
import abc
from typing import Callable, List


# pylint: disable=too-few-public-methods
class VcdElements(abc.ABC):
    """Classes to return from parser"""


# pylint: disable=too-few-public-methods
class EndOfFile(abc.ABC):
    """The files have finished"""


class AggregatorInterface(abc.ABC):
    """Classes to return from parser"""
    @abc.abstractmethod
    def get_list(self) -> List['VcdElements']:
        """Return elements until end-of-file"""

    @abc.abstractmethod
    def namespace(self) -> str:
        """Return namespace of this aggregator"""


class InputOutputManager:
    """Manages the entire data-flow"""
    def __init__(self, in_files: List[str],
                 factory: Callable[[str], AggregatorInterface],
                 ofiles: List[str], enable_diff: bool):
        self.readers = [factory(i) for i in in_files]

    def run(self):
        """Run configured readers and writers"""
        elements = [list() for _ in range(len(self.readers))]
        while self._all_readers_empty(elements):
            pass

    def _all_readers_empty(self, elements: List) -> bool:
        all_empty = True
        for i, reader in enumerate(self.readers):
            element = reader.get_list()
            elements[i] = element
            if len(element) == 1 and isinstance(element[0], EndOfFile):
                all_empty = False
        return all_empty
