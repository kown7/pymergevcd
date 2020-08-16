"""Provide test fixtures"""
import logging
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


# pylint: disable=too-many-locals
@pytest.fixture
def src_merge_file(tmpdir):
    """Create two vcd files with random data and the expected, merged result"""
    src1 = os.path.sep.join([str(tmpdir), 'src1.vcd'])
    src2 = os.path.sep.join([str(tmpdir), 'src2.vcd'])
    dest = os.path.sep.join([str(tmpdir), 'test_merged.vcd'])
    with open(src1, 'w+') as ptr1, open(
            src2, 'w+') as ptr2, open(dest, 'w+') as dest_fp:
        with vcd.VCDWriter(
                dest_fp, timescale=(10, 'ns'), date='today'
        ) as dest_wr, vcd.VCDWriter(
            ptr1, timescale=(10, 'ns'), date='today'
        ) as src1_wr, vcd.VCDWriter(ptr2, timescale=(10, 'ns'),
                                    date='today') as src2_wr:
            counter_merge = dest_wr.register_var(src1[:-4], 'foobar',
                                                 'integer', size=32)
            bartwo_merge = dest_wr.register_var(src1[:-4] + '.a', 'bar_two',
                                                'reg', size=16)
            counter8_merge = dest_wr.register_var(src1[:-4] + '.a', 'counter',
                                                  'integer', size=8)
            lcounter_merge = dest_wr.register_var(src2[:-4], 'foobar2',
                                                  'integer', size=32)
            logging.info('%s.a', src1[:-4])

            counter_var1 = src1_wr.register_var('', 'foobar', 'integer',
                                                size=32)
            bartwo_var1 = src1_wr.register_var('a', 'bar_two', 'reg', size=16)
            counter8_var1 = src1_wr.register_var('a', 'counter', 'integer',
                                                 size=8)

            lcounter_var2 = src2_wr.register_var('', 'foobar2', 'integer',
                                                 size=32)

            timestamp = 1
            for i in range(1000, 10_000, 100):
                src1_wr.change(counter_var1, timestamp, i)
                src1_wr.change(bartwo_var1, timestamp, i % 2)
                src1_wr.change(counter8_var1, timestamp, i % 256)
                dest_wr.change(counter_merge, timestamp, i)
                dest_wr.change(bartwo_merge, timestamp, i % 2)
                dest_wr.change(counter8_merge, timestamp, i % 256)
                if timestamp >= 20:
                    src2_wr.change(lcounter_var2, timestamp, i - 20)
                    dest_wr.change(lcounter_merge, timestamp, i - 20)
                timestamp += 1

    return (src1, src2, dest)
