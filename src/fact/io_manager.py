"""Manage input"""
from typing import List

import fact.vcd_reader
import fact.vcd_writer
import fact.merge_engine


class InputOutputManager:
    """Manages the entire data-flow"""
    def merge_files(self, in_files: List[str], ofile: str):
        """Merge the files given in in_files to ofile"""
        readers = [fact.vcd_reader.factory(i) for i in in_files]
        writer = fact.vcd_writer.factory(ofile)
        mergee = fact.merge_engine.MergeEngine(readers)
        writer.process_source(mergee)
