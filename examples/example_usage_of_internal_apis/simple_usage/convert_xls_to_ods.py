"""
convert_xls_to_ods.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows how to use **Book** and **BookWriter** class to convert
xls file to ods file.

What this example implies is that you can do the conversion in
between these formats:
==== === === === ==== ====
     ods csv xls xlsx xlsm
==== === === === ==== ====
ods  y   y   y   y    y       
csv  y   y   y   y    y   
xls  y   y   y   y    y   
xlsx y   y   y   y    y   
xlsm y   y   y   y    y   
---- --- --- --- ---- ----
"""
import os
import pyexcel as pe
# you will need to install pyexcel-ods or pyexcel-ods3
# depending on your python version
import pyexcel.ext.xls
import pyexcel.ext.ods3


def main(base_dir):
    # Simple open the file using Book
    book = pe.Book(filename="multiple-sheets.xls")
    
    # Create a new book by creating a BookWriter instance
    newbook = pe.BookWriter("multiple-sheets.ods")
    
    # Now simple state you want to save the content of
    # book to newbook
    newbook.write_book_reader(book)
    
    # Close the writer
    newbook.close()
    
    # then you will have the book in ods

if __name__ == '__main__':
    main(os.getcwd())