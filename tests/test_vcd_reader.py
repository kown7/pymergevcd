"""Test basic VCD file parsing"""
import pytest

import pymergevcd.io_manager_interfaces as iomi
import pymergevcd.vcd_reader


def test_end_of_file(record_property, dummy_vcd_file):
    """Test if data is read and it all ends with an End-Of-File

    * SW-AS-200: assert `VcdReader` is an `AggregatorInterface`
    * SW-AS-201: assert a list of `iomi.VcdElements` is returned
    * Sw-AS-202: assert last element is `iomi.VcdElements`

    """
    record_property('req', 'SW-AS-200-b85e5b1b')
    record_property('req', 'SW-AS-201-eb13fc0f')
    record_property('req', 'SW-AS-202-35354cd8')
    vcdr = pymergevcd.vcd_reader.VcdReader(dummy_vcd_file)
    assert isinstance(vcdr, iomi.AggregatorInterface)
    baseidx = 2
    entries = vcdr.get_list()
    assert isinstance(entries[0], iomi.VcdDate)
    assert isinstance(entries[1], iomi.VcdTimescale)
    assert isinstance(entries[baseidx], iomi.VcdVariable)
    assert entries[baseidx].name == 'dummyvar'
    assert entries[baseidx + 1].scope == 'a'
    assert entries[baseidx + 2].scope == 'a.b.c'
    assert isinstance(entries[-1], iomi.VcdEndOfFile)
    entries = vcdr.get_list()
    assert isinstance(entries[0], iomi.VcdEndOfFile)


def test_factory(dummy_vcd_file):
    """See if factory returns the correct objects"""
    with pytest.raises(ValueError):
        pymergevcd.vcd_reader.factory(dummy_vcd_file + '.txt')
    assert isinstance(pymergevcd.vcd_reader.factory(dummy_vcd_file),
                      pymergevcd.vcd_reader.VcdReader)
