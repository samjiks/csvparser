import unittest

from csvparser import CSVParser, NotValidCSVFileError

class TestCSVParser(unittest.TestCase):

    def test_csv_parser(self):
        csvp = CSVParser('1.txt')
        assert csvp.filename == '1.txt'
        assert  csvp.mode == 'rt'

    def test_file_invalid_csv(self):
        with CSVParser('a.txt'):
            self.assertRaises(NotValidCSVFileError)

    def test_file_exists(self):
        with CSVParser('csv'):
            self.assertRaises(FileNotFoundError)

    def test_field_names(self):
        with CSVParser('csv_files/1.csv', 'rt') as cp:
            expected = ['mon', 'tue', 'some_column1', 'wed', 'thu', 'fri', 'description']
            cp.get_field_names() == expected

    def test_current_file_func(self):
        with CSVParser('csv_files/1.csv', 'rt') as cp:
            assert cp.get_current_file == 'csv_files/1.csv'

