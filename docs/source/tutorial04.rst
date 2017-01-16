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
    sheet3:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+

or via array notations:

    >>> book["sheet 1"] # there is a space in the sheet name
    sheet 1:
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

   >>> import glob
   >>> merged = pyexcel.Sheet()
   >>> for file in glob.glob("*.csv"):
   ...     merged.row += pyexcel.get_sheet(file_name=file)
   >>> merged.save_as("merged.csv")

How do I read a book, process it and save to a new book
--------------------------------------------------------------------------------

Yes, you can do that. The code looks like this::

   import pyexcel

   book = pyexcel.get_book(file_name="yourfile.xls")
   for sheet in book:
       # do you processing with sheet
       # do filtering?
       pass
   book.save_as("output.xls")
 
What would happen if I save a multi sheet book into "csv" file
--------------------------------------------------------------------------------

Well, you will get one csv file per each sheet. Suppose you have these code:

.. code-block:: python

   >>> content = {
   ...     'Sheet 1': 
   ...         [
   ...             [1.0, 2.0, 3.0], 
   ...             [4.0, 5.0, 6.0], 
   ...             [7.0, 8.0, 9.0]
   ...         ],
   ...     'Sheet 2': 
   ...         [
   ...             ['X', 'Y', 'Z'], 
   ...             [1.0, 2.0, 3.0], 
   ...             [4.0, 5.0, 6.0]
   ...         ], 
   ...     'Sheet 3': 
   ...         [
   ...             ['O', 'P', 'Q'], 
   ...             [3.0, 2.0, 1.0], 
   ...             [4.0, 3.0, 2.0]
   ...         ] 
   ... }
   >>> book = pyexcel.Book(content)
   >>> book.save_as("myfile.csv")

You will end up with three csv files:

.. code-block:: python

   >>> import glob
   >>> outputfiles = glob.glob("myfile_*.csv")
   >>> for file in sorted(outputfiles):
   ...     print(file)
   ...
   myfile__Sheet 1__0.csv
   myfile__Sheet 2__1.csv
   myfile__Sheet 3__2.csv

and their content is the value of the dictionary at the corresponding key


.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("myfile__Sheet 1__0.csv")
   >>> os.unlink("myfile__Sheet 2__1.csv")
   >>> os.unlink("myfile__Sheet 3__2.csv")

Alternatively, you could use :meth:`~pyexcel.save_book_as` function

.. code-block:: python

   >>> pyexcel.save_book_as(bookdict=content, dest_file_name="myfile.csv")


After I have saved my multiple sheet book in csv format, how do I get them back
--------------------------------------------------------------------------------

First of all, you can read them back individual as csv file using `meth:~pyexcel.get_sheet` method. Secondly, the pyexcel can do
the magic to load all of them back into a book. You will just need to provide the common name before the separator "__":

.. code-block:: python

    >>> book2 = pyexcel.get_book(file_name="myfile.csv")
    >>> book2
    Sheet 1:
    +-----+-----+-----+
    | 1.0 | 2.0 | 3.0 |
    +-----+-----+-----+
    | 4.0 | 5.0 | 6.0 |
    +-----+-----+-----+
    | 7.0 | 8.0 | 9.0 |
    +-----+-----+-----+
    Sheet 2:
    +-----+-----+-----+
    | X   | Y   | Z   |
    +-----+-----+-----+
    | 1.0 | 2.0 | 3.0 |
    +-----+-----+-----+
    | 4.0 | 5.0 | 6.0 |
    +-----+-----+-----+
    Sheet 3:
    +-----+-----+-----+
    | O   | P   | Q   |
    +-----+-----+-----+
    | 3.0 | 2.0 | 1.0 |
    +-----+-----+-----+
    | 4.0 | 3.0 | 2.0 |
    +-----+-----+-----+
    
.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("myfile__Sheet 1__0.csv")
   >>> os.unlink("myfile__Sheet 2__1.csv")
   >>> os.unlink("myfile__Sheet 3__2.csv")
   >>> os.unlink("book.xls")
   >>> os.unlink("book1.xls")
   >>> os.unlink("book2.xlsx")
   >>> os.unlink("merged.csv")
