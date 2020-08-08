"""Merge one or more VCD files"""
import logging
from typing import List

import fact.io_manager_interfaces as iomi


class MergeEngine(iomi.AggregatorInterface):
    """Merge multiple files"""

    def __init__(self, sources: List[iomi.AggregatorInterface]):
        self.sources: List[iomi.AggregatorInterface] = sources

    # pylint: disable=too-many-branches
    def get_list(self) -> List[iomi.VcdElements]:  # noqa: C901
        """Return elements until end-of-file

        It's a monster of function that extracts all exisiting
        elements. It then proceeds to sort all elements in-memory.

        """
        elements_arr = dict()
        for i in self.sources:
            j = i.get_list()
            logging.info('Length of list: %i', len(j))
            elements_arr[i] = j
            while not isinstance(j[-1], iomi.VcdEndOfFile):
                j = i.get_list()
                logging.info('Length of list: %i', len(j))
                elements_arr[i].extend(j)

        for i in self.sources:
            if not isinstance(elements_arr[i][0], iomi.VcdEndOfFile):
                break
        else:
            return elements_arr[i]

        header: List[iomi.VcdElements] = []
        values: List[iomi.VcdValueChange] = []
        timescale = None
        for i in self.sources:
            for element in elements_arr[i]:
                if isinstance(element, iomi.VcdValueChange):
                    element.ident = i.namespace() + element.ident
                    values.append(element)
                if isinstance(element, iomi.VcdVariable):
                    element.scope = i.namespace() + '.' + element.scope
                    element.ident = i.namespace() + element.ident
                    header.append(element)
                if isinstance(element, iomi.VcdTimescale):
                    assert timescale is None or (
                        element.size == timescale.size
                        and element.units == timescale.units), \
                        "Timescales are different, doesn't merge atm"
                    timescale = element

        assert timescale is not None
        return ([timescale] + header +                      # type: ignore
                sorted(values, key=lambda x: x.timestamp))  # type: ignore

    def namespace(self) -> str:
        """Return namespace of this aggregator"""
        return 'MergeEngine'
