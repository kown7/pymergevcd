"""Test IO handling"""
import fact.io_manager
import fact.vcd_reader


def test_basic_run(dummy_vcd_file):
    """See if run terminates"""
    app = fact.io_manager.InputOutputManager(
        [dummy_vcd_file, dummy_vcd_file],
        fact.vcd_reader.factory, 'test.vcd', False)
    app.run()
