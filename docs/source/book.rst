Book
=========

You access each cell via this syntax::

    book[sheet_index][row, column]

or::

    book["sheet_name"][row, column]

Suppose you have the following sheets:

.. pyexcel-table::

   ---pyexcel:Sheet 1---
   1,2,3
   4,5,6
   7,8,9
   ---pyexcel---
   ---pyexcel:Sheet 2---
   X,Y,Z
   1,2,3
   4,5,6
   ---pyexcel---
   ---pyexcel:Sheet 3---
   O,P,Q
   3,2,1
   4,3,2

.. testcode::
   :hide:

   >>> import pyexcel
   >>> data = {
   ...      'Sheet 1':
   ...          [
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0],
   ...              [7.0, 8.0, 9.0]
   ...          ],
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
   ...          ]
   ...  }
   >>> book = pyexcel.Book(data)
   >>> book.save_as("example.xls")

And you can randomly access a cell in a sheet::

    >>> book = pyexcel.get_book(file_name="example.xls")
    >>> print(book["Sheet 1"][0,0])
    1
    >>> print(book[0][0,0]) # the same cell
    1

.. TIP::
  With pyexcel, you can regard single sheet as an
  two dimensional array and multi-sheet excel book
  as an ordered dictionary of two dimensional arrays.

**Write multiple sheet excel book**

Suppose you have previous data as a dictionary and you want to 
save it as multiple sheet excel file::

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
    >>> book = pyexcel.get_book(bookdict=content)
    >>> book.save_as("output.xls")

You shall get a xls file


**Read multiple sheet excel file**

Let's read the previous file back:

    >>> book = pyexcel.get_book(file_name="output.xls")
    >>> sheets = book.to_dict()
    >>> for name in sheets.keys():
    ...     print(name)
    Sheet 1
    Sheet 2
    Sheet 3

Get content
************

.. code-block:: python

    >>> book_dict = {
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
    >>> book = pyexcel.get_book(bookdict=book_dict)
    >>> book
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
    >>> print(book.rst)
    Sheet 1:
    =  =  =
    1  2  3
    4  5  6
    7  8  9
    =  =  =
    Sheet 2:
    ===  ===  ===
    X    Y    Z
    1.0  2.0  3.0
    4.0  5.0  6.0
    ===  ===  ===
    Sheet 3:
    ===  ===  ===
    O    P    Q
    3.0  2.0  1.0
    4.0  3.0  2.0
    ===  ===  ===

You can get the direct access to underneath stream object. In some situation,
it is desired.


.. code-block:: python

    >>> stream = book.stream.plain

The returned stream object has the content formatted in plain format
for further reading.


Set content
************

Surely, you could set content to an instance of :class:`pyexcel.Book`.

.. code-block:: python

    >>> other_book = pyexcel.Book()
    >>> other_book.bookdict = book_dict
    >>> print(other_book.plain)
    Sheet 1:
    1  2  3
    4  5  6
    7  8  9
    Sheet 2:
    X    Y    Z
    1.0  2.0  3.0
    4.0  5.0  6.0
    Sheet 3:
    O    P    Q
    3.0  2.0  1.0
    4.0  3.0  2.0

You can set via 'xls' attribute too.

.. code-block:: python

    >>> another_book = pyexcel.Book()
    >>> another_book.xls = other_book.xls
    >>> print(another_book.mediawiki)
    Sheet 1:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | align="right"| 1 || align="right"| 2 || align="right"| 3
    |-
    | align="right"| 4 || align="right"| 5 || align="right"| 6
    |-
    | align="right"| 7 || align="right"| 8 || align="right"| 9
    |}
    Sheet 2:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | X || Y || Z
    |-
    | 1 || 2 || 3
    |-
    | 4 || 5 || 6
    |}
    Sheet 3:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | O || P || Q
    |-
    | 3 || 2 || 1
    |-
    | 4 || 3 || 2
    |}



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

You also can merge individual sheets::

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
   >>> os.unlink("output.xls")
