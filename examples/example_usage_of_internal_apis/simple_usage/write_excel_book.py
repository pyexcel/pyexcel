"""
read_excel_book.py
:copyright: (c) 2014-2015 by C. W.
:license: GPL v3

This shows how to use **BookWriter** class to write a dictionary
to sheet spreadsheet.
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

# Now simply choose the filename and format you want to save
# file format is decided by the file extension
w=pe.BookWriter("multiple-sheets.xls")
# A call to write the dictionary
w.write_book_from_dict(data)
# Now close the file
w.close()

# The output of the file is "mltiple-sheets.xls"
