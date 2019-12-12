"""Provide test fixtures"""
import os

import pytest
import vcd


@pytest.fixture
def dummy_vcd_file(tmpdir):
    """Create vcd file with random data"""
    filename = os.path.sep.join([str(tmpdir), 'test.vcd'])
    with open(filename, 'w+') as fptr:
        with vcd.VCDWriter(fptr, timescale=(10, 'ns'), date='today') as writer:
            counter_var = writer.register_var('', 'dummyvar', 'integer',
                                              size=8)
            counter3_var = writer.register_var('a', 'dummyvara', 'integer')
            counter_var = writer.register_var('a.b.c', 'counter', 'integer',
                                              size=8)
            for i in range(1000, 300000, 300):
                timestamp = 0
                for timestamp, value in enumerate(range(10, 200, 2)):
                    writer.change(counter_var, i + timestamp, value)
                writer.change(counter3_var, i + timestamp, i % 42)
    return filename
