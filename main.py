import os
import glob
import csv

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv_files')


class NotValidDayError(Exception):
    pass


def get_csv_files(directory=None):
    return glob.iglob((directory or DEFAULT_DATA_DIR) + '/*.csv')

class Parser(object):

    DAYS_OF_WEEK = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    def __init__(self, filename, mode='rt'):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        try:
            self.open_file = open(self.filename, self.mode)
        except FileNotFoundError:
            print("file not found")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.open_file.close()

    def get_field_names(self):
        reader = csv.DictReader(self.open_file)
        fieldnames = reader.fieldnames
        return fieldnames

    def get_rows(self):
        try:
            reader = csv.DictReader(self.open_file)
            for row in reader:
                yield row, self.open_file
        except Exception as e:
            print(e)

    @staticmethod
    def square(value):
        if value:
            return int(value) ** 2

    @staticmethod
    def double(value):
        if value:
            return int(value) * 2

    @staticmethod
    def character_between_day(field, delimiter='-'):
        return delimiter in field

    def split_day(self, field, delimiter='-'):
        return field.split(delimiter)[0:2]

    def _get_field_value(self, day, value):
        try:
            cal = self.get_cal_type(day)
        except NotValidDayError:
            pass
        else:
            return self._build_fields(day=day, value=value, cal=cal)

    def get_cal_type(self, day):
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

    def parse(self):
        for rows, file in self.get_rows():
            for field, value in rows.items():
                if self.character_between_day(field):
                    split_fields = self.split_day(field)
                    for field in split_fields:
                        print(self._get_field_value(field, value))
                elif field in self.DAYS_OF_WEEK:
                        print(self._get_field_value(field, value))
            print(file)

if __name__ == '__main__':
    for f in get_csv_files():
        with Parser(f) as p:
            p.parse()


