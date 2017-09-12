import unittest
from mock import mock_open, patch

from csvparser import CSVParser

class TestCSVParser(unittest.TestCase):

    def test_csv_parser(self):
        csvp = CSVParser('1.txt')
        assert csvp.filename == '1.txt'
        assert  csvp.mode == 'rt'

    def test_file_open(self):
        m = mock_open()
        with patch('{}.open'.format(__name__), m, create=True):
            with CSVParser('foo', 'rt') as h:
                h.get_rows()
        m.assert_called_once_with('foo', 'w')