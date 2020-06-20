"""Test IO handling"""
import filecmp

import fact.io_manager


def test_simple_io(record_property, dummy_vcd_file):
    """Feed it through unchanged and expect the same file"""
    record_property("req", "SW-AS-501-44d4ac79")
    ofile = 'test.vcd'
    iom = fact.io_manager.InputOutputManager()
    iom.merge_files([dummy_vcd_file], ofile)
    assert filecmp.cmp(dummy_vcd_file, ofile)


def test_read_write_engines(record_property, dummy_vcd_file):
    """Write-back from read file, equal output"""
    record_property("req", "SW-AS-501-44d4ac79")
    ofile = 'test_writeback.vcd'
    reader = fact.vcd_reader.factory(dummy_vcd_file)
    writer = fact.vcd_writer.factory(ofile)

    writer.process_source(reader)
    assert filecmp.cmp(dummy_vcd_file, ofile)
