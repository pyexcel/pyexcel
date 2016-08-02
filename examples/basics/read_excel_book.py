"""
read_excel_book.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows how to use get_book to go through a multiple
sheet spreadsheet.

Please install pyexcel-ods3
"""
import os
import pyexcel as pe


def main(base_dir):
    # Simply give a name to the Book class
    book = pe.get_book(file_name=os.path.join(base_dir,
                                              "multiple-sheets-example.ods"))

    # the default iterator for a **Book* instance is a SheetIterator
    for sheet in book:
        # Each sheet has name
        print("sheet: %s" % sheet.name)
        # Once you have a sheet instance, you can regard it as
        # a Reader instance. You can iterate its member in the way
        # you wanted it
        for row in sheet:
            print(row)


if __name__ == '__main__':
    main(os.getcwd())
# Here's the output
# sheet: Sheet 2
# [u'X', u'Y', u'Z']
# [1.0, 2.0, 3.0]
# [4.0, 5.0, 6.0]
# sheet: Sheet 3
# [u'O', u'P', u'Q']
# [3.0, 2.0, 1.0]
# [4.0, 3.0, 2.0]
# sheet: Sheet 1
# [1.0, 2.0, 3.0]
# [4.0, 5.0, 6.0]
# [7.0, 8.0, 9.0]
