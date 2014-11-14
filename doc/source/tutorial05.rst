Data manipulation in a sheet
============================

The data in a sheet is represented by :class:`Matrix` which maintains the data as a list of lists. You can regard :class:`Matrix` as a two dimensional array with additional iterators. Random access to individual column and row is explosed by class:`Column` and class:`Row` 

Column manipulation with SeriesReader
-------------------------------------

Suppose have one data file as the following:

.. table:: file "example.xls"

    ======== ======== ========
    Column 1 Column 2 Column 3
    ======== ======== ========
    1        4        7
    2        5        8
    3        6        9
    ======== ======== ========

.. testcode::
   :hide:

   >>> import pyexcel
   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 4, 7],
   ...      [2, 5, 8],
   ...      [3, 6, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

	
And you want to update ``Column 2`` with these data: [11, 12, 13]

Here is the code::

   >>> sheet = pyexcel.load("example.xls", name_columns_by_row=0)
   >>> sheet.column["Column 2"] = [11, 12, 13]
   >>> sheet.column[1]
   [11, 12, 13]

Example output:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        11       7
2        12       8
3        13       9
======== ======== ========

Remove one column of a data file
*********************************

If you want to remove ``Column 2``, you can just call::

   >>> del sheet.column["Column 2"]
   >>> sheet.column["Column 3"]
   [7.0, 8.0, 9.0]

The sheet content will become:

.. table:: sheet content

    ======== ========
    Column 1 Column 3
    ======== ========
    1        7
    2        8
    3        9
    ======== ========


Append more columns to a data file
---------------------------------

Continue from previous example. Suppose you want add two more columns to the data file

======== ========
Column 4 Column 5
======== ========
10       13
11       14
12       15
======== ========

Here is the example code to append two extra columns::

    >>> extra_data = [
    ...    ["Column 4", "Column 5"],
    ...    [10, 13],
    ...    [11, 14],
    ...    [12, 15]
    ... ]
    >>> sheet2 = pyexcel.Sheet(extra_data)
    >>> sheet.column += sheet2
    >>> sheet.column["Column 4"]
    [10, 11, 12]
    >>> sheet.column["Column 5"]
    [13, 14, 15]

Here is what you will get:

======== ======== ======== ========
Column 1 Column 3 Column 4 Column 5
======== ======== ======== ========
1        7        10       13       
2        8        11       14       
3        9        12       15       
======== ======== ======== ========

