"""Regression tests from real-world examples"""
import pytest

import pymergevcd.io_manager


@pytest.mark.manual
def test_regression_two_files(record_property):
    """Trying to merge two files

    Currently not publicly available source files, hence no good test.

    """
    record_property('req', 'SW-AS-nnn-deadbeef')
    ifile1 = 'tests/Test_Datenpfad2_LE0_A_1_a_expected.vcd'
    ifile2 = 'tests/Test_Datenpfad2_LE0_A_1_a_given.vcd'
    ofile = 'test_regression_two_files.vcd'
    iom = pymergevcd.io_manager.InputOutputManager()
    iom.merge_files([ifile1, ifile2], ofile)
    assert True
