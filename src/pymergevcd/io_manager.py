"""Manage input"""
from typing import List, Optional

import pymergevcd.io_manager_interfaces as iomi
import pymergevcd.merge_engine
import pymergevcd.vcd_reader
import pymergevcd.vcd_writer


# pylint: disable=too-few-public-methods
class InputOutputManager:
    """Manages the entire data-flow"""

    @staticmethod
    def merge_files(in_files: List[str], ofile: str,
                    datestr: Optional[str] = None):
        """Merge the files given in in_files to ofile.

        Set the `date` in the merged VCD file to `datestr` if
        given.

        """
        readers: List[iomi.AggregatorInterface] = [
            pymergevcd.vcd_reader.factory(i) for i in in_files]
        writer = pymergevcd.vcd_writer.factory(ofile)
        mergee = pymergevcd.merge_engine.MergeEngine(readers, datestr)
        writer.process_source(mergee)
