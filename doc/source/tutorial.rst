Simple usage
=============

Random access to individual cell
--------------------------------

To randaomly access a cell of :class:`~pyexcel.Sheet` instance, two syntax are avaialbe::

    sheet[row, column]

or

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

   >>> import pyexcel

.. testcode::
   :hide:

   >>> data = [['Example', 'X', 'Y', 'Z'], ['a', 1, 2, 3],['b', 4, 5, 6],['c', 7, 8, 9]]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

.. testcode::

   >>> sheet = pyexcel.load("example.xls""")
   >>> print(sheet[2, 2])
   5.0
   >>> print(sheet["C3"])
   5.0


Random access to rows and columns
---------------------------------

.. testcode::
   :hide:

   >>> sheet[1, 0] = str(sheet[1, 0])
   >>> str(sheet[1,0])
   'a'
   >>> sheet[0, 2] = str(sheet[0, 2])
   >>> sheet[0,2]
   'Y'

Continue with previous excel file, you can access row and column separately::

    >>> sheet.row[1]
    ['a', 1.0, 2.0, 3.0]
    >>> sheet.column[2]
    ['Y', 2.0, 5.0, 8.0]


Use custom names instead of index
---------------------------------
Alternatively, it is possible to use the first row to refer to each columns::

    >>> sheet.name_columns_by_row(0)
    >>> print(sheet[1, "Y"])
    5.0

You have noticed the row index has been changed. It is because first row is taken as the column names, hence all rows after the first row are shifted. Now accessing the columns are changed too::

    >>> sheet.column['Y']
    [2.0, 5.0, 8.0]

Hence access the same cell, this statement also works::

    >>> sheet.column['Y'][1]
    5.0
  
Further more, it is possible to use first column to refer to each rows::

    >>> sheet.name_rows_by_column(0)

To access the same cell, we can use this line::

    >>> sheet.row["b"][1]
    5.0

For the same reason, the row index has been reduced by 1. Since we have named columns and rows, it is possible to access the same cell like this::

    >>> print(sheet["b", "Y"])
    5.0

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

    >>> book = pyexcel.load_book("example.xls")
    >>> print(book["Sheet 1"][0,0])
    1.0
    >>> print(book[0][0,0]) # the same cell
    1.0

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
    >>> sheet = pyexcel.load("example.xls")
    >>> print(json.dumps(sheet.to_array()))
    [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

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
   >>> sheet = pyexcel.load("example_series.xls", name_columns_by_row=0)

.. testcode::
   :hide:

   >>> sheet._column_names = [ str(name) for name in sheet._column_names]

.. testcode::

    >>> sheet.to_dict()
    OrderedDict([('Column 1', [1.0, 4.0, 7.0]), ('Column 2', [2.0, 5.0, 8.0]), ('Column 3', [3.0, 6.0, 9.0])])

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
    >>> sheet = pyexcel.load("example.xls", name_columns_by_row=0)
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
    1.0


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
    >>> content = pyexcel.utils.dict_to_array(example_dict)
    >>> # "output.xls" "output.xlsx" "output.ods" "output.xlsm"
    >>> sheet = pyexcel.Sheet(content)
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
    >>> book = pyexcel.Book(content)
    >>> book.save_as("output.xls")

You shall get a xls file


Read multiple sheet excel file
------------------------------

Let's read the previous file back:
    
    >>> book = pyexcel.load_book("output.xls")
    >>> sheets = book.to_dict()
    >>> for name in sheets.keys():
    ...     print(name)
    Sheet 1
    Sheet 2
    Sheet 3

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("output.xls")
   >>> os.unlink("output.csv")
   >>> os.unlink("example.xls")
   >>> os.unlink("example_series.xls")
