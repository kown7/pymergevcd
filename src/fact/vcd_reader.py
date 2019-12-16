"""Parse a VCD file into its elements"""
import abc
import logging
from typing import List

import vcd
from fact.io_manager import AggregatorInterface, EndOfFile  # noqa:I100


class VcdElements(abc.ABC):
    """Classes to return from parser"""


class VcdEndOfFile(VcdElements, EndOfFile):
    """Signal end-of-file"""


class VcdTimescale(VcdElements):
    """Configured Timescale"""
    def __init__(self, size, units):
        assert 1000 >= int(size) > 0
        assert units in vcd.VCDWriter.TIMESCALE_UNITS
        self.size = size
        self.units = units


class VcdDate(VcdElements):
    """Configured Date"""
    def __init__(self, date):
        self.data = date


class VcdVariable(VcdElements):
    """Variable"""
    def __init__(self, scope, name, var_type, ident, size=None, init=None):
        self.scope = scope
        self.name = name
        self.ident = ident
        self.var_type = var_type
        self.size = size
        self.init = init


class VcdValueChange(VcdElements):
    """New value for `VcdVariable`"""
    def __init__(self, line: list):
        if len(line) == 1:
            self.value = line[0][0]
            self.ident = line[0][0]  # Identifier
        elif len(line) == 2:
            self.value = line[0]
            self.ident = line[1]
        else:
            raise ValueError


class VcdParserState:
    """Store current parse information and create new `VcdElements`"""
    def __init__(self):
        self.tstamp = 0
        self.register = dict()
        self.scope = []
        self.parsing_values = False

    def factory(self, line: str) -> VcdElements:  # noqa:C901
        """Convert lines into VcdElements

        Default values are currently not supported. Rather they are
        interpreted as the value at t = 0.

        """
        linel = line.split(' ')
        if line[0] == '#':
            self.tstamp = int(line[1:].strip())
        elif linel[0] == '$timescale':
            return VcdTimescale(linel[1], linel[2])
        elif linel[0] == '$date':
            return VcdDate(linel[1])
        elif linel[0] == '$var':
            size = int(linel[2])
            return VcdVariable('.'.join(self.scope), linel[4], linel[1],
                               linel[3], size)
        elif linel[0] == '$scope':
            if linel[2]:
                logging.info('Scope: %s %s', linel[2], linel[3])
                self.scope.append(linel[2])
        elif linel[0] == '$upscope':
            if self.scope:
                del self.scope[-1]
            else:
                logging.warning('Scope empty')
            logging.info(self.scope)
        elif linel[0] == '$dumpvars':
            self.parsing_values = True
        elif linel[0] in ('$enddefinitions'):
            pass
        elif self.parsing_values:
            VcdValueChange(linel)
        else:
            raise KeyError('Unknown Key in VCD File')
        return None


class VcdReader(AggregatorInterface):
    """Parse a VCD file into `VcdElements`"""
    def __init__(self, filename: str = None):
        """Parse given filename"""
        self._filename = filename
        self._elements = []
        self._is_parsed = False
        self._parse()

    def get_list(self) -> List[VcdElements]:
        """Return all elements of file"""
        if self._elements:
            cur_el = self._elements[:]
            del self._elements[:len(cur_el)]
            logging.info('Returning %i elements', len(cur_el))
            return cur_el
        if self._is_parsed:
            return [VcdEndOfFile()]
        return []

    def namespace(self) -> str:
        return self._filename

    def _parse(self):
        logging.info('Starting parsing')
        state = VcdParserState()
        for line in open(self._filename):
            parsed_line = state.factory(line.strip())
            if parsed_line:
                self._elements.append(parsed_line)
        self._elements.append(VcdEndOfFile())
        self._is_parsed = True
        logging.info('Terminating parsing: %i elements', len(self._elements))


def factory(filename: str) -> VcdReader:
    """Create an `AggregatorInterface` reader depending on filename"""
    if filename.endswith('.vcd'):
        return VcdReader(filename)
    raise ValueError('Unexpected file-ending')
