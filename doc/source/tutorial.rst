Simple usage
=============

Random access to individual cell
--------------------------------

For single sheet file, you can regard it as two dimensional array. So, you access each cell via this syntax: reader[row, column]. Suppose you have the following data, you can get value 5 by reader[1, 1].

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
   >>> print sheet[2, 2]
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

For multiple sheet file, you can regard it as three dimensional array if you use `Book`. So, you access each cell via this syntax: reader[sheet_index][row][column] or reader["sheet_name"][row][column]. Suppose you have the following sheets. You can get 'P' from sheet 3 by using: bookreader["Sheet 3"][0][1] or bookreader[2][0][1]


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

The following code will give you the data in json::

    from pyexcel
    import json
    
    # "example.xls","example.xlsx","example.xlsm"
    sheet = pyexcel.load("example.csv")
    print json.dumps(sheet.to_array()


The output is::

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

The following code will give you data series in a dictionary:

.. code-block:: python

    from pyexcel as pe
    
    # "example.xls","example.xlsx","example.xlsm"
    sheet = pe.load("example.csv", name_columns_by_row=0)
    print(sheet.to_dict())


The output is::

    {"Column 1": [1, 2, 3], "Column 2": [4, 5, 6], "Column 3": [7, 8, 9]}

Can I get an array of dictionaries per each row?
*************************************************

Returning to previous example:

= = =
X Y Z
1 2 3
4 5 6
7 8 9
= = =

The following code will produce what you want::

    from pyexcel as pe
    import json
    
    # "example.xls","example.xlsx","example.xlsm"
    reader = pe.load("example.csv", name_columns_by_row=0)
    print json.dumps(data.to_record())


The output is::

    [{"X":1, "Y":2, "Z":3}, {"X":4 ...}, ... ]


Writing a single sheet excel file
---------------------------------

Suppose you have an array as the following:

= = =
1 2 3
4 5 6
7 8 9
= = =

The following code will write it as an excel file of your choice::


    from pyexcel as pe
    
    array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # "output.xls" "output.xlsx" "output.ods" "output.xlsm"
	sheet = pe.Sheet(array)
    sheet.save_as("output.csv")


Suppose you have a dictionary as the following:

======== ========= ========
Column 1 Column 2  Column 3
======== ========= ========
1        4         7
2        5         8
3        6         9
======== ========= ========

The following code will write it as an excel file of your choice::

    from pyexcel as pe
    
    example_dict = {"Column 1": [1, 2, 3], "Column 2": [4, 5, 6], "Column 3": [7, 8, 9]}
    # "output.xls" "output.xlsx" "output.ods" "output.xlsm"
	book = pe.Book(example_dict)
    book.save_as("output.csv")


Read multiple sheet excel file
------------------------------

Suppose you have a book like this:

= = =
1 2 3
4 5 6
7 8 9
= = =

Sheet 1

= = =
X Y Z
1 2 3
4 5 6
= = =

Sheet 2

= = =
O P Q
3 2 1
4 3 2
= = =

Sheet 3

You can get a dictionary out of it by the following code::

    import pyexcel as pe
    
    
    book = pe.load_book("example.xls")
    print(book.to_dict())

the output is::

    {
    u'Sheet 1': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
    u'Sheet 2': [[u'X', u'Y', u'Z'], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], 
    u'Sheet 3': [[u'O', u'P', u'Q'], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]]
    }


Write multiple sheet excel file
-------------------------------

Suppose you have previous data as a dictionary and you want to save it as multiple sheet excel file::

    import pyexcel as pe
    
    
    content = {
        'Sheet 1': 
            [
                [1.0, 2.0, 3.0], 
                [4.0, 5.0, 6.0], 
                [7.0, 8.0, 9.0]
            ],
        'Sheet 2': 
            [
                ['X', 'Y', 'Z'], 
                [1.0, 2.0, 3.0], 
                [4.0, 5.0, 6.0]
            ], 
        'Sheet 3': 
            [
                ['O', 'P', 'Q'], 
                [3.0, 2.0, 1.0], 
                [4.0, 3.0, 2.0]
            ] 
    }
    book = pe.Book(content)
    book.save_as("output.xls")

You shall get a xls file 
