"""
write_excel_book.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows how to use **Book** class to write a dictionary
to sheet spreadsheet.

Please install pyexcel-xls.

"""
import pyexcel as pe

# the dictionary should look like the following:
#  * key: a string typed key
#  * value: a two dimensional array or a list of lists
data={
    "Sheet 1": [[1,2,3],[4,5,6],[7,8,9]],
    "Sheet 2": [['X', 'Y', 'Z'], [1,2,3],[4,5,6]],
    "Sheet 3": [['O', 'P', 'Q'], [3,2,1],[4,3,2]]
}
# In order to keep the order of the sheets, please use OrderedDict

# Now simply choose the filename and format you want to save
# file format is decided by the file extension
book = pe.Book(data)

# simple save it
book.save_as("multiple-sheets.xls")

# The output of the file is "multiple-sheets.xls"
