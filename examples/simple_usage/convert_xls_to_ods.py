"""
convert_xls_to_ods.py
:copyright: (c) 2014 by C. W.
:license: GPL v3

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
import pyexcel as pe
# you will need to install pyexcel-ods or pyexcel-ods3
# depending on your python version
from pyexcel.ext import ods

# Simple open the file using Book
book = pe.Book("multiple-sheets.xls")

# Create a new book by creating a BookWriter instance
newbook = pe.BookWriter("multiple-sheets.ods")

# Now simple state you want to save the content of
# book to newbook
newbook.write_book_reader(book)

# Close the writer
newbook.close()

# then you will have the book in ods