"""Test basic VCD file parsing"""
import pytest
import fact.vcd_reader


def test_end_of_file(dummy_vcd_file):
    """Test if data is read and it all ends with an End-Of-File"""
    vcdr = fact.vcd_reader.VcdReader(dummy_vcd_file)
    baseidx = 2
    entries = vcdr.get_list()
    assert isinstance(entries[0], fact.vcd_reader.VcdDate)
    assert isinstance(entries[1], fact.vcd_reader.VcdTimescale)
    assert isinstance(entries[baseidx], fact.vcd_reader.VcdVariable)
    assert entries[baseidx].name == 'dummyvar'
    assert entries[baseidx + 1].scope == 'a'
    assert entries[baseidx + 2].scope == 'a.b.c'
    assert isinstance(entries[-1], fact.vcd_reader.VcdEndOfFile)
    entries = vcdr.get_list()
    assert isinstance(entries[0], fact.vcd_reader.VcdEndOfFile)


def test_factory(dummy_vcd_file):
    """See if factory returns the correct objects"""
    with pytest.raises(ValueError):
        fact.vcd_reader.factory(dummy_vcd_file + '.txt')
    assert isinstance(fact.vcd_reader.factory(dummy_vcd_file),
                      fact.vcd_reader.VcdReader)