"""Merge one or more VCD files"""
from typing import List, Optional
import logging

import fact.io_manager_interfaces as iomi


class MergeEngine(iomi.AggregatorInterface):
    """Merge multiple files"""

    def __init__(self, sources: Optional[List[iomi.AggregatorInterface]] = []):
        self.sources: List[iomi.AggregatorInterface] = sources

    # pylint: disable=too-many-branches
    def get_list(self) -> List[iomi.VcdElements]:
        """Return elements until end-of-file"""
        elements_arr = dict()
        for i in self.sources:
            j = i.get_list()
            logging.info("Length of list: %i", len(j))
            elements_arr[i] = j
            while not isinstance(j[-1], iomi.VcdEndOfFile):
                j = i.get_list()
                logging.info("Length of list: %i", len(j))
                elements_arr[i].extend(j)

        for i in self.sources:
            if not isinstance(elements_arr[i][0], iomi.VcdEndOfFile):
                break
        else:
            return elements_arr[i]

        header = []
        values = []
        timescale = None
        for i in self.sources:
            for element in elements_arr[i]:
                if isinstance(element, iomi.VcdValueChange):
                    element.ident = i.namespace() + element.ident
                    values.append(element)
                if isinstance(element, iomi.VcdVariable):
                    element.scope = i.namespace() + "." + element.scope
                    element.ident = i.namespace() + element.ident
                    header.append(element)
                if isinstance(element, iomi.VcdTimescale):
                    assert timescale is None or (
                        element.size == timescale.size
                        and element.units == timescale.units), \
                        "Timescales are different, doesn't merge atm"
                    timescale = element

        assert timescale is not None
        return [timescale] + header + sorted(values, key=lambda x: x.timestamp)

    def namespace(self) -> str:
        """Return namespace of this aggregator"""
        return "MergeEngine"
