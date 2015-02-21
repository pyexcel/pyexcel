"""
read_row_by_row.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows a pythonic way to use **Reader** class to go through a single
page spreadsheet row by row. The output is::

    [1.0, 2.0, 3.0]
    [4.0, 5.0, 6.0]
    [7.0, 8.0, 9.0]

"""
import pyexcel

# "example.csv","example.xlsx","example.ods", "example.xlsm"
spreadsheet = pyexcel.Reader("example.xls") 

# rows() returns row based iterator, meaning it can be iterated row by row
for row in spreadsheet.rows():
    print row

# Alternatively, you can use::
#   for row in spreadsheet:
#       print row
# because by default **Reader** regards itself a row based iterator.


