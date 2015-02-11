"""
read_row_by_row.py
:copyright: (c) 2014-2015 by C. W.
:license: GPL v3

This shows a pythonic way to use **Reader** class to go through a single
page spreadsheet column by column. The output is::

    [1.0, 4.0, 7.0]
    [2.0, 5.0, 8.0]
    [3.0, 6.0, 9.0]

"""
import pyexcel as pe

# "example.csv","example.ods","example.xls", "example.xlsm"
spreadsheet = pe.load("example.xlsx") 

# columns() returns column based iterator, meaning it can be iterated
# column by column 
for value in spreadsheet.columns():
    print value