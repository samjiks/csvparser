import unittest

from csvparser import CSVParser, WeedDayParser, NotValidCSVFileError

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

    def test_is_csv_file_func(self):
            f = 'csv_files/1.csv'
            with CSVParser(f, 'rt') as cp:
                assert cp.is_csv_file(f) == True

            f = 'csv_files/5.csv'
            with CSVParser(f, 'rt'):
                self.assertRaises(NotValidCSVFileError)


class TestWeekDayCSVParser(unittest.TestCase):

    def test_parent_class(self):
        wdp = WeedDayParser('1.txt')
        assert wdp.__class__.__bases__[0] == CSVParser

