"""Test IO handling"""
import filecmp

import pymergevcd.io_manager


def test_simple_io(record_property, dummy_vcd_file):
    """Feed it through unchanged and expect the "same" file

    The date and scope of the files will have changed accordingly.

    """
    record_property('req', 'SW-AS-501-44d4ac79')
    ofile = 'test_merge.vcd'
    iom = pymergevcd.io_manager.InputOutputManager()
    iom.merge_files([dummy_vcd_file], ofile)
    assert (len(open(dummy_vcd_file).readlines()) ==
            len(open(ofile).readlines()))


def test_read_write_engines(record_property, dummy_vcd_file):
    """Write-back from read file, equal output"""
    record_property('req', 'SW-AS-501-44d4ac79')
    ofile = 'test_writeback.vcd'
    reader = pymergevcd.vcd_reader.factory(dummy_vcd_file)
    writer = pymergevcd.vcd_writer.factory(ofile)

    writer.process_source(reader)
    assert filecmp.cmp(dummy_vcd_file, ofile)


def test_merge_two_files(record_property, src_merge_file):
    """Merge two files with given return expected answer"""
    record_property('req', 'SW-AS-1-7d6734f3')
    ofile = 'merge_two_files.vcd'
    iom = pymergevcd.io_manager.InputOutputManager()
    iom.merge_files([src_merge_file[0], src_merge_file[1]],
                    ofile, 'today')
    assert filecmp.cmp(src_merge_file[2], ofile)
