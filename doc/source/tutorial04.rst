
Book: Sheet operations
=========================

Access to individual sheets
-----------------------------

.. testcode::
   :hide:

   >>> import pyexcel
   >>> data = {
   ...      'sheet 1':
   ...          [
   ...              [1.0, 2.0, 3.0],
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0]
   ...          ],
   ...      'sheet2':
   ...          [
   ...              ['O', 'P', 'Q'],
   ...              [3.0, 2.0, 1.0],
   ...              [4.0, 3.0, 2.0]
   ...          ],
   ...      'sheet3':
   ...          [
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0],
   ...              [7.0, 8.0, 9.0]
   ...          ]
   ...  }
   >>> pyexcel.save_book_as(bookdict=data, dest_file_name="book.xls")

You can access individual sheet of a book via attribute:

    >>> book = pyexcel.get_book(file_name="book.xls")
    >>> book.sheet3
    Sheet Name: sheet3
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+

or via array notations:

    >>> book["sheet 1"] # there is a space in the sheet name
    Sheet Name: sheet 1
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+


Merge excel books
----------------------

Suppose you have two excel books and each had three sheets. You can merge them and get a new book:

.. testcode::
   :hide:

   >>> data = {
   ...      'Sheet 2':
   ...          [
   ...              ['X', 'Y', 'Z'],
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0]
   ...          ],
   ...      'Sheet 3':
   ...          [
   ...              ['O', 'P', 'Q'],
   ...              [3.0, 2.0, 1.0],
   ...              [4.0, 3.0, 2.0]
   ...          ],
   ...      'Sheet 1':
   ...          [
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0],
   ...              [7.0, 8.0, 9.0]
   ...          ]
   ...  }
   >>> book = pyexcel.Book(data)
   >>> book.save_as("book1.xls")
   >>> book.save_as("book2.xlsx")

You also can merge indivdual sheets::

   >>> book1 = pyexcel.get_book(file_name="book1.xls")
   >>> book2 = pyexcel.get_book(file_name="book2.xlsx")
   >>> merged_book = book1 + book2
   >>> merged_book = book1["Sheet 1"] + book2["Sheet 2"]
   >>> merged_book = book1["Sheet 1"] + book2
   >>> merged_book = book1 + book2["Sheet 2"]


Manipulate individual sheets
-----------------------------

merge sheets into a single sheet
*********************************

Suppose you want to merge many csv files row by row into a new sheet.

   >>> import pyexcel as pe 
   >>> import glob
   >>> merged = pyexcel.Sheet()
   >>> for file in glob.glob("*.csv"):
   ...     merged.row += pe.get_sheet(file_name=file)
   >>> merged.save_as("merged.csv")

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("book.xls")
   >>> os.unlink("book1.xls")
   >>> os.unlink("book2.xlsx")
   >>> os.unlink("merged.csv")
