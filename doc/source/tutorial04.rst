Excel Book Manipulations
=========================

Merge excel books
----------------------

Suppose you have two excel books and each had three sheets. You can merge them and get a new book::

    >>> import pyexcel.Book
    >>> merged_book = Book("book1.xls") + Book("book2.ods")

You also can merge indivdual sheets::

    >>> merged_book = Book("book1.xls")["Sheet1"] + Book("book2.ods")["Sheet2"]

or::

    >>> merged_book = Book("book1.xls")["Sheet1"] + Book("book2.ods")

or::

    >>> merged_book = Book("book1.xls") + Book("book2.ods")["Sheet2"]


Manipulate individual sheets
-----------------------------

merge sheets into a single sheet
*********************************

Suppose you want to merge many csv files row by row into a new sheet.

    >>> import pyexcel
    >>> import glob
    >>> merged = pyexcel.Reader()
    >>> for file in glob.glob("*.csv"):
    >>>     merged += pyexcel.Reader(file)
    >>> writer = pyexcel.Writer("merged.csv")
    >>> writer.write_reader(merged)
    >>> writer.close()
