Book: Sheet operations
=========================

Merge excel books
----------------------

Suppose you have two excel books and each had three sheets. You can merge them and get a new book::

   >>> import pyexcel

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

   >>> book1 = pyexcel.load_book("book1.xls")
   >>> book2 = pyexcel.load_book("book2.xlsx")
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
   ...     merged.row += pe.load(file)
   >>> writer = pe.Writer("merged.csv")
   >>> writer.write_reader(merged)
   >>> writer.close()

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("book1.xls")
   >>> os.unlink("book2.xlsx")
