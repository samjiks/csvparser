import os
import sys
import glob
import csv

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'csv_files')


class NotValidDayError(Exception):
    pass


class NotValidCSVFileError(Exception):
    pass


def get_csv_files(directory=None):
    return glob.iglob((directory or DEFAULT_DATA_DIR) + '/*.csv')


class CSVParser(object):

    def __init__(self, filename, mode='rt'):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        try:
            if self.is_csv_file(self.get_current_file):
                self.open_file = open(self.get_current_file, self.mode)
        except NotValidCSVFileError:
            print('Not Valid CSV File')
        except FileNotFoundError:
            print("file not found")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.open_file.close()

    @property
    def get_current_file(self):
        return self.filename

    @staticmethod
    def is_csv_file(f):
        if f.endswith('csv'):
            return True
        else:
            raise NotValidCSVFileError

    def get_field_names(self):
        reader = csv.DictReader(self.open_file)
        fieldnames = reader.fieldnames
        return fieldnames

    def get_rows(self):
        try:
            reader = csv.DictReader(self.open_file)
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)
        else:
            for row in reader:
                yield row

    def parse_filename(self):
        if self.filename.index('/') != -1:
            return self.filename.rsplit('/')[-1]
        else:
            return self.filename


class WeedDayParser(CSVParser):

    DAYS_OF_WEEK = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    def __init__(self, filename, mode='rt'):
        super().__init__(filename, mode)

    @staticmethod
    def square(value):
        if value:
            return int(value) ** 2

    @staticmethod
    def double(value):
        if value:
            return int(value) * 2

    @staticmethod
    def _has_bar_between_days(field, delimiter='-'):
        return delimiter in field

    def split_day(self, field, delimiter='-'):
        return field.split(delimiter)[0:2]

    def _get_field_value(self, day, value):
        try:
            cal = self.get_mode(day)
        except NotValidDayError:
            print('Cell does not contain a Day')
        else:
            return self._build_fields(day=day, value=value, cal=cal)

    def get_mode(self, day):
        if day in ['mon', 'tue', 'wed']:
            return self.square
        elif day in ['thu', 'fri']:
            return self.double
        raise NotValidDayError

    def _build_fields(self, day, value, cal):
        build = {
            'day': day,
            'value': value,
        }
        c = (cal(value) if cal is not None else "")

        if cal == self.square:
            build['square'] = c
        elif cal == self.double:
             build['double'] = c

        return build

    def iter_through_days(self, fields):
        between_days = []
        for field in fields:
            try:
                index = self.DAYS_OF_WEEK.index(field)
            except IndexError:
                    print('No such field %s', field)
            else:
                between_days.append(index)
        if len(between_days) != 2:
            print('Not have enough days to process')
        else:
            return between_days

    def _get_field_value_between_days(self, day_index, value):
        try:
            for index in range(day_index[0], day_index[1]+1):
                print(self._get_field_value(self.DAYS_OF_WEEK[index], value))
        except ValueError as e:
            print(e)

    def parse(self):
        for rows in self.get_rows():
            sys.stdout.write(self.parse_filename() + '\n')
            for field, value in rows.items():
                if self._has_bar_between_days(field):
                    split_fields = self.split_day(field)
                    between_days = self.iter_through_days(split_fields)
                    self._get_field_value_between_days(between_days, value)
                elif field in self.DAYS_OF_WEEK:
                    print(self._get_field_value(field, value))
                else:
                    pass
                    # TODO: Need to work with Description flattening


