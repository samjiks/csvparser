from csvparser import get_csv_files, WeedDayParser

if __name__ == '__main__':
    for f in get_csv_files():
        with WeedDayParser(f) as p:
            p.parse()
