Sheet: Data Access
===================

Iterate a csv file
----------------------------

Here is the way to read the csv file and iterate through each row:

.. testcode::
   :hide:

   >>> import pyexcel
   >>> pyexcel.save_as(array=[['Name', 'Age'], ['Chu Chu', '10'], ['Mo mo', '11']],
   ...     dest_file_name='tutorial.csv')

.. code-block:: python

    >>> sheet = pyexcel.get_sheet(file_name='tutorial.csv')
    >>> for row in sheet:
    ...     print("%s: %s" % (row[0], row[1]))
    Name: Age
    Chu Chu: 10
    Mo mo: 11

Often people wanted to use csv.Dict reader to read it because it has a header. Here
is how you do it with pyexcel:

.. code-block:: python
   :linenos:

   >>> sheet = pyexcel.get_sheet(file_name='tutorial.csv')
   >>> sheet.name_columns_by_row(0)
   >>> for row in sheet:
   ...     print("%s: %s" % (row[0], row[1]))
   Chu Chu: 10
   Mo mo: 11

Line 2 remove the header from the actual content. The removed header can be used
to access its columns using the name itself, for example:

.. code-block:: python

   >>> sheet.column['Age']
   [10, 11]

.. _access-to-cell:

Random access to individual cell
--------------------------------

To randomly access a cell of :class:`~pyexcel.Sheet` instance, two syntax are available::

    sheet[row, column]

or::

    sheet['A1']

The former syntax is handy when you know the row and column numbers. The latter syntax is introduced to help you convert the excel column header such as "AX" to integer numbers.

Suppose you have the following data, you can get value 5 by reader[2, 2].

======= = = =
Example X Y Z
a       1 2 3
b       4 5 6
c       7 8 9
======= = = =


Here is the example code showing how you can randomly access a cell::

.. testcode::
   :hide:

   >>> data = [['Example', 'X', 'Y', 'Z'], ['a', 1, 2, 3],['b', 4, 5, 6],['c', 7, 8, 9]]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

.. testcode::

   >>> sheet = pyexcel.get_sheet(file_name="example.xls")
   >>> sheet.content
   +---------+---+---+---+
   | Example | X | Y | Z |
   +---------+---+---+---+
   | a       | 1 | 2 | 3 |
   +---------+---+---+---+
   | b       | 4 | 5 | 6 |
   +---------+---+---+---+
   | c       | 7 | 8 | 9 |
   +---------+---+---+---+
   >>> print(sheet[2, 2])
   5
   >>> print(sheet["C3"])
   5
   >>> sheet[3, 3] = 10
   >>> print(sheet[3, 3])
   10

.. note::

   In order to set a value to a cell, please use sheet[row_index, column_index] = new_value


Random access to rows and columns
---------------------------------

.. testcode::
   :hide:

   >>> sheet[1, 0] = str(sheet[1, 0])
   >>> str(sheet[1,0])
   'a'
   >>> sheet[0, 2] = str(sheet[0, 2])
   >>> sheet[0, 2]
   'Y'

Continue with previous excel file, you can access row and column separately::

    >>> sheet.row[1]
    ['a', 1, 2, 3]
    >>> sheet.column[2]
    ['Y', 2, 5, 8]


Use custom names instead of index
---------------------------------
Alternatively, it is possible to use the first row to refer to each columns::

    >>> sheet.name_columns_by_row(0)
    >>> print(sheet[1, "Y"])
    5
    >>> sheet[1, "Y"] = 100
    >>> print(sheet[1, "Y"])
    100

You have noticed the row index has been changed. It is because first row is taken as the column names, hence all rows after the first row are shifted. Now accessing the columns are changed too::

    >>> sheet.column['Y']
    [2, 100, 8]

Hence access the same cell, this statement also works::

    >>> sheet.column['Y'][1]
    100

Further more, it is possible to use first column to refer to each rows::

    >>> sheet.name_rows_by_column(0)

To access the same cell, we can use this line::

    >>> sheet.row["b"][1]
    100

For the same reason, the row index has been reduced by 1. Since we have named columns and rows, it is possible to access the same cell like this::

    >>> print(sheet["b", "Y"])
    100
    >>> sheet["b", "Y"] = 200
    >>> print(sheet["b", "Y"])
    200

.. note::

   When you have named your rows and columns, in order to set a value to a cell, please use sheet[row_name, column_name] = new_value


For multiple sheet file, you can regard it as three dimensional array if you use :class:`~pyexcel.Book`. So, you access each cell via this syntax::

    book[sheet_index][row, column]

or::

    book["sheet_name"][row, column]

Suppose you have the following sheets:

.. table:: Sheet 1

    = = =
    1 2 3
    4 5 6
    7 8 9
    = = =

.. table:: Sheet 2

    = = =
    X Y Z
    1 2 3
    4 5 6
    = = =

.. table:: Sheet 3

    = = =
    O P Q
    3 2 1
    4 3 2
    = = =

.. testcode::
   :hide:

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
  With pyexcel, you can regard single sheet reader as an two dimensional array and multi-sheet excel book reader as a ordered dictionary of two dimensional arrays.


Reading a single sheet excel file
---------------------------------
Suppose you have a csv, xls, xlsx file as the following:

= = =
1 2 3
4 5 6
7 8 9
= = =

.. testcode::
   :hide:

   >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

The following code will give you the data in json::

    >>> import json
    >>> # "example.csv","example.xlsx","example.xlsm"
    >>> sheet = pyexcel.get_sheet(file_name="example.xls")
    >>> print(json.dumps(sheet.to_array()))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

Read the sheet as a dictionary
******************************
Suppose you have a csv, xls, xlsx file as the following:

======== ========= ========
Column 1 Column 2  Column 3
======== ========= ========
1        4         7
2        5         8
3        6         9
======== ========= ========

.. testcode::
   :hide:

   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 2, 3],
   ...      [4, 5, 6],
   ...      [7, 8, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example_series.xls")


The following code will give you data series in a dictionary:

.. testcode::

   >>> # "example.xls","example.xlsx","example.xlsm"
   >>> sheet = pyexcel.get_sheet(file_name="example_series.xls", name_columns_by_row=0)

.. testcode::
   :hide:

   >>> sheet.colnames = [ str(name) for name in sheet.colnames]

.. testcode::

    >>> sheet.to_dict()
    OrderedDict([('Column 1', [1, 4, 7]), ('Column 2', [2, 5, 8]), ('Column 3', [3, 6, 9])])

Can I get an array of dictionaries per each row?
*************************************************

Suppose you have the following data:

= = =
X Y Z
1 2 3
4 5 6
7 8 9
= = =

.. testcode::
   :hide:

   >>> data = [['X', 'Y', 'Z'], [1, 2, 3],[4, 5, 6],[7, 8, 9]]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

The following code will produce what you want::

    >>> # "example.csv","example.xlsx","example.xlsm"
    >>> sheet = pyexcel.get_sheet(file_name="example.xls", name_columns_by_row=0)
    >>> records = sheet.to_records()
    >>> for record in records:
    ...     keys = sorted(record.keys())
    ...     print("{")
    ...     for key in keys:
    ...         print("'%s':%d" % (key, record[key]))
    ...     print("}")
    {
    'X':1
    'Y':2
    'Z':3
    }
    {
    'X':4
    'Y':5
    'Z':6
    }
    {
    'X':7
    'Y':8
    'Z':9
    }
    >>> print(records[0]["X"]) # access first row and first item
    1


Writing a single sheet excel file
---------------------------------

Suppose you have an array as the following:

= = =
1 2 3
4 5 6
7 8 9
= = =

The following code will write it as an excel file of your choice::


.. testcode::


    >>> array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> # "output.xls" "output.xlsx" "output.ods" "output.xlsm"
    >>> sheet = pyexcel.Sheet(array)
    >>> sheet.save_as("output.csv")


Suppose you have a dictionary as the following:

======== ========= ========
Column 1 Column 2  Column 3
======== ========= ========
1        4         7
2        5         8
3        6         9
======== ========= ========

The following code will write it as an excel file of your choice::


    >>> example_dict = {"Column 1": [1, 2, 3], "Column 2": [4, 5, 6], "Column 3": [7, 8, 9]}
    >>> # "output.xls" "output.xlsx" "output.ods" "output.xlsm"
    >>> sheet = pyexcel.get_sheet(adict=example_dict)
    >>> sheet.save_as("output.csv")


Write multiple sheet excel file
-------------------------------

Suppose you have previous data as a dictionary and you want to save it as multiple sheet excel file::

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


Read multiple sheet excel file
------------------------------

Let's read the previous file back:

    >>> book = pyexcel.get_book(file_name="output.xls")
    >>> sheets = book.to_dict()
    >>> for name in sheets.keys():
    ...     print(name)
    Sheet 1
    Sheet 2
    Sheet 3

Work with data series in a single sheet
---------------------------------------

Suppose you have the following data in any of the supported excel formats again:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========


.. testcode::

   >>> sheet = pyexcel.get_sheet(file_name="example_series.xls", name_columns_by_row=0)

.. testcode::
   :hide:

   >>> sheet.colnames = [ str(name) for name in sheet.colnames]


Play with data
**************

You can get headers::

    >>> print(list(sheet.colnames))
    ['Column 1', 'Column 2', 'Column 3']

You can use a utility function to get all in a dictionary::

    >>> sheet.to_dict()
    OrderedDict([('Column 1', [1, 4, 7]), ('Column 2', [2, 5, 8]), ('Column 3', [3, 6, 9])])

Maybe you want to get only the data without the column headers. You can call :meth:`~pyexcel.Sheet.rows()` instead::

    >>> list(sheet.rows())
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

You can get data from the bottom to the top one by calling :meth:`~pyexcel.Sheet.rrows()` instead::

    >>> list(sheet.rrows())
    [[7, 8, 9], [4, 5, 6], [1, 2, 3]]

You might want the data arranged vertically. You can call :meth:`~pyexcel.Sheet.columns()` instead::

    >>> list(sheet.columns())
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

You can get columns in reverse sequence as well by calling :meth:`~pyexcel.Sheet.rcolumns()` instead::

    >>> list(sheet.rcolumns())
    [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

Do you want to flatten the data? You can get the content in one dimensional array. If you are interested in playing with one dimensional enumeration, you can check out these functions :meth:`~pyexcel.Sheet.enumerate`, :meth:`~pyexcel.Sheet.reverse`, :meth:`~pyexcel.Sheet.vertical`, and :meth:`~pyexcel.Sheet.rvertical()`::

    >>> list(sheet.enumerate())
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> list(sheet.reverse())
    [9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> list(sheet.vertical())
    [1, 4, 7, 2, 5, 8, 3, 6, 9]
    >>> list(sheet.rvertical())
    [9, 6, 3, 8, 5, 2, 7, 4, 1]



.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("output.xls")
   >>> os.unlink("output.csv")
   >>> os.unlink("example.xls")
   >>> os.unlink("example_series.xls")
