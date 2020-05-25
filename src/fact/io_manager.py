"""Manage input"""
from typing import Callable, List

import fact.io_manager_interfaces as iomi


class InputOutputManager:
    """Manages the entire data-flow"""
    def __init__(self, in_files: List[str],
                 factory: Callable[[str], iomi.AggregatorInterface],
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
            if len(element) == 1 and isinstance(element[0], iomi.EndOfFile):
                all_empty = False
        return all_empty
