"""Test Event Merging"""
import fact.io_manager
import fact.io_manager_interfaces as iomi


def test_elements_out_of_merge_engine(record_property, dummy_vcd_file):
    """Ensure the headers are correctly ordered

    We need a timestamp element that is not none.

    """
    record_property('req', 'SW-AS-400-deadbeef')
    readers = [fact.vcd_reader.factory(dummy_vcd_file),
               fact.vcd_reader.factory(dummy_vcd_file)]
    mergee = fact.merge_engine.MergeEngine(readers)
    vcd_elements = mergee.get_list()
    has_header = False
    for i in vcd_elements:
        if isinstance(i, iomi.VcdTimescale):
            assert i.size is not None
            assert i.units is not None
            has_header = True
    assert has_header


def test_merge_engine_single_file(record_property, dummy_vcd_file):
    """Ensure the headers are correctly ordered

    We need a timestamp element that is not none.

    We are getting wrong data in upper-level merge order

    """
    record_property('req', 'SW-AS-400-deadbeef')
    readers = [fact.vcd_reader.factory(dummy_vcd_file)]
    mergee = fact.merge_engine.MergeEngine(readers)
    vcd_elements = mergee.get_list()
    has_header = False
    for i in vcd_elements:
        if isinstance(i, iomi.VcdTimescale):
            assert i.size is not None
            assert i.units is not None
            has_header = True
    assert has_header
    assert isinstance(vcd_elements[-2], iomi.VcdValueChange)
    assert isinstance(vcd_elements[-1], iomi.VcdValueChange)
    assert isinstance(mergee.get_list()[0], iomi.VcdEndOfFile)
