# pylint: disable=too-few-public-methods
"""Interface definitions for IO Manager"""
import abc
from typing import List

import vcd


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


class WriterInterface(abc.ABC):
    """Classes to return from parser"""
    @abc.abstractmethod
    def process_source(self, src: AggregatorInterface):
        """Process an AggregatorInterface source

        Args:
           src: AggregatorInterface source, possibly VcdReaders

    """


class EndOfFile(abc.ABC):
    """The files have finished"""


class VcdEndOfFile(VcdElements, EndOfFile):
    """Signal end-of-file"""


class VcdTimescale(VcdElements):
    """Configured Timescale"""
    def __init__(self, size, units):
        assert 1000 >= int(size) > 0
        assert units in [
            x.value for x in vcd.writer.TimescaleUnit.__members__.values()]
        self.size = size
        self.units = units


class VcdDate(VcdElements):
    """Configured Date"""
    def __init__(self, date):
        self.date = date


class VcdEndOfHeader(VcdElements):
    """Indicate Header Parsing is over, data follows"""


class VcdVariable(VcdElements):
    """Variable"""
    # pylint: disable=too-many-arguments
    def __init__(self, scope, name, var_type, ident, size=None, init=None):
        self.scope = scope
        self.name = name
        self.ident = ident
        self.var_type = var_type
        self.size = size
        self.init = init


class VcdValueChange(VcdElements):
    """New value for `VcdVariable`"""
    def __init__(self, line: list, tstamp: int):
        self.timestamp = tstamp
        if len(line) == 1:
            self.value = line[0][0]
            self.ident = line[0][1:]  # Identifier
        elif len(line) == 2:
            self.value = line[0]
            self.ident = line[1]
        else:
            raise ValueError

        if isinstance(self.value, str) and self.value[0] == 'b':
            if self.value[1] == 'x':
                self.value = self.value[1:]
            else:
                self.value = int(self.value[1:], 2)
