#!/usr/bin/env python

import os
import tempfile
import unittest

import docverter


def _test_converter(to, format=None, extra_args=()):

    def reader(*args, **kwargs):
        return source, format

    def processor(*args):
        return 'ok'

    source = 'foo'

    return docverter._convert(
        reader, processor, source, to, format, extra_args)


class TestDocverter(unittest.TestCase):
    def test_converts_valid_format(self):
        self.assertEqual(_test_converter(format='md', to='rest'), 'ok')

    def test_does_not_convert_to_invalid_format(self):
        try:
            _test_converter(format='md', to='invalid')
        except RuntimeError:
            pass

    def test_does_not_convert_from_invalid_format(self):
        try:
            _test_converter(format='invalid', to='rest')
        except RuntimeError:
            pass

    def test_basic_conversion_from_file(self):
        # This will not work on windows:
        # http://docs.python.org/2/library/tempfile.html
        with tempfile.NamedTemporaryFile('w+t', suffix='.md',
                                         delete=False) as test_file:
            file_name = test_file.name
            print('test_file = %r' % test_file)
            print('file_name = %r' % file_name)
            test_file.write('#some title\n')
            test_file.flush()
            expected = 'some title{0}=========={0}{0}'.format(os.linesep)
            received = docverter.convert(file_name, 'rst')
            self.assertEqualExceptForNewlineEnd(expected, received)

    def test_basic_conversion_from_file_with_format(self):
        # This will not work on windows:
        # http://docs.python.org/2/library/tempfile.html
        with tempfile.NamedTemporaryFile('w+t', suffix='.rst',
                                         delete=False) as test_file:
            file_name = test_file.name
            print('test_file = %r' % test_file)
            print('file_name = %r' % file_name)
            test_file.write('#some title\n')
            test_file.flush()
            expected = 'some title{0}=========={0}{0}'.format(os.linesep)
            received = docverter.convert(file_name, 'rst', format='md')
            self.assertEqualExceptForNewlineEnd(expected, received)

    def test_basic_conversion_from_string(self):
        expected = 'some title{0}=========={0}{0}'.format(os.linesep)
        received = docverter.convert('#some title', 'rst', format='md')
        self.assertEqualExceptForNewlineEnd(expected, received)

    def assertEqualExceptForNewlineEnd(self, expected, received):
        self.assertEqual(expected.rstrip('\n'), received.rstrip('\n'))
