"""
read_column_by_column.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows a pythonic way to use **Reader** class to go through a single
page spreadsheet column by column. The output is::

    [1.0, 4.0, 7.0]
    [2.0, 5.0, 8.0]
    [3.0, 6.0, 9.0]

"""
import os
import pyexcel

def main(base_dir):
    # "example.csv","example.ods","example.xls", "example.xlsm"
    spreadsheet = pyexcel.Reader(os.path.join(base_dir, "example.xlsx"))
    
    # columns() returns column based iterator, meaning it can be iterated
    # column by column 
    for value in spreadsheet.columns():
        print(value)


if __name__ == '__main__':
    main(os.getcwd())