"""Parse a VCD file into its elements"""
import logging
from typing import List, Optional

import pymergevcd.io_manager_interfaces as iomi


# pylint: disable=too-few-public-methods
class VcdParserState:
    """Store current parse information and create new `VcdElements`"""
    def __init__(self):
        self.tstamp = 0
        self.register = dict()
        self.scope = []
        self.parsing_values = False

    # pylint: disable=too-many-branches
    def factory(self, line: str) -> Optional[iomi.VcdElements]:  # noqa:C901
        """Convert lines into VcdElements

        Default values are currently not supported. Rather they are
        interpreted as the value at t = 0.

        """
        linel = line.split(' ')
        if line[0] == '#':
            self.tstamp = int(line[1:].strip())
        elif linel[0] == '$timescale':
            return iomi.VcdTimescale(linel[1], linel[2])
        elif linel[0] == '$date':
            return iomi.VcdDate(linel[1])
        elif linel[0] == '$var':
            size = int(linel[2])
            return iomi.VcdVariable('.'.join(self.scope), linel[4], linel[1],
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
        elif linel[0] == '$end':
            assert self.parsing_values is True
        elif linel[0] in ['$enddefinitions']:
            return iomi.VcdEndOfHeader()
        elif self.parsing_values:
            return iomi.VcdValueChange(linel, self.tstamp)
        else:
            raise KeyError('Unknown Key in VCD File')
        return None


class VcdReader(iomi.AggregatorInterface):
    """Parse a VCD file into `VcdElements`"""
    def __init__(self, filename: str = ''):
        """Parse given filename"""
        self._filename = filename
        self._elements: List[iomi.VcdElements] = []
        self._is_parsed = False
        self._parse()

    def get_list(self) -> List[iomi.VcdElements]:
        """Return all elements of file"""
        if self._elements:
            cur_el = self._elements[:]
            del self._elements[:len(cur_el)]
            logging.info('Returning %i elements', len(cur_el))
            return cur_el
        if self._is_parsed:
            return [iomi.VcdEndOfFile()]
        return []

    def namespace(self) -> str:
        if self._filename[-4:] == '.vcd':
            namespace = self._filename[:-4]
        namespace = namespace.replace('.', '_')
        return namespace

    def _parse(self):
        logging.info('Starting parsing')
        state = VcdParserState()
        for line in open(self._filename):
            parsed_line = state.factory(line.strip())
            if parsed_line:
                self._elements.append(parsed_line)
        self._elements.append(iomi.VcdEndOfFile())
        self._is_parsed = True
        logging.info('Terminating parsing: %i elements', len(self._elements))


def factory(filename: str) -> VcdReader:
    """Create an `AggregatorInterface` reader depending on filename"""
    if filename.endswith('.vcd'):
        return VcdReader(filename)
    raise ValueError('Unexpected file-ending')
