"""Write the streams of `VcdElements` back into files"""
import logging
from typing import List

import vcd

import pymergevcd.io_manager_interfaces as iomi


# pylint: disable=too-few-public-methods
class VcdComposer:
    """Create VCD file from `VcdElements` objects"""
    def __init__(self, fptr):
        self._fptr = fptr
        self._date = None
        self._timescale = None
        self._vars = dict()
        self.__vw = None

    @property
    def _vw(self):
        """VCDWriter object with all things"""
        if self.__vw is None and self._timescale is not None:
            logging.info('Setting up VCDWriter')
            self.__vw = vcd.VCDWriter(self._fptr,
                                      timescale=self._timescale,
                                      date=self._date)
        return self.__vw

    def add_elements(self, elements: List[iomi.VcdElements]):
        """Add list of `VcdElements` to the output file

        Generally the output from the `get_list` call.

        """
        for element in elements:
            if isinstance(element, iomi.VcdTimescale):
                self._timescale = (str(element.size) + ' ' + element.units)
                logging.info(self._timescale)
            elif isinstance(element, iomi.VcdDate):
                self._date = element.date
            elif isinstance(element, iomi.VcdVariable):
                i = self._vw.register_var(element.scope,
                                          element.name,
                                          element.var_type,
                                          size=element.size,
                                          init=element.init)
                self._vars[element.ident] = i
            elif isinstance(element, iomi.VcdValueChange):
                self._vw.change(self._vars[element.ident], element.timestamp,
                                element.value)
            elif isinstance(element, iomi.VcdEndOfFile):
                return False
        return True


class VcdWriter(iomi.WriterInterface):
    """Parse a VCD file into `VcdElements`"""
    def __init__(self, filename: str = ''):
        """Parse given filename"""
        assert filename
        self._filename = filename
        self._src: iomi.AggregatorInterface

    def process_source(self, src: iomi.AggregatorInterface):
        """Add a source and process its content"""
        self._src = src
        with open(self._filename, 'w+') as fptr:
            self._process(fptr)

    def _process(self, fptr):
        logging.info('Starting parsing')
        state = VcdComposer(fptr)
        suc = True
        while suc:
            elements = self._src.get_list()
            assert isinstance(elements, list)
            suc = state.add_elements(elements)
            logging.info('Terminating processing: %i elements', len(elements))


def factory(filename: str) -> VcdWriter:
    """Create an `WriterInterface` writer for given filename"""
    if filename.endswith('.vcd'):
        return VcdWriter(filename)
    raise ValueError('Unexpected file-ending')
