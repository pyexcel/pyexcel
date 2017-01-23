"""
read_column_by_column.py
:copyright: (c) 2014-2017 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows a pythonic way to use get_sheet to go through a single
page spreadsheet column by column. The output is::

    [1.0, 4.0, 7.0]
    [2.0, 5.0, 8.0]
    [3.0, 6.0, 9.0]

"""
import os
import pyexcel as pe


def main(base_dir):
    # "example.csv","example.ods","example.xls", "example.xlsm"
    spreadsheet = pe.get_sheet(file_name=os.path.join(base_dir,
                                                      "example.xlsx"))

    # columns() returns column based iterator, meaning it can be iterated
    # column by column
    for value in spreadsheet.columns():
        print(value)


if __name__ == '__main__':
    main(os.getcwd())
