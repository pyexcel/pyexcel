==============================
Work with excel files
==============================

.. WARNING::

    The pyexcel DOES NOT consider Fonts, Styles, Formulas and Charts at all. When you load a stylish excel and update it, you definitely will lose all those.

Add a new row to an existing file
----------------------------------

Suppose you have one data file as the following:

example.xls

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

.. testcode::
   :hide:

   >>> import os
   >>> import pyexcel
   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 4, 7],
   ...      [2, 5, 8],
   ...      [3, 6, 9]
   ...  ]
   >>> pyexcel.save_as(array=data, dest_file_name="example.xls")

And you want to add a new row:

    12, 11, 10

Here is the code:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_sheet(file_name="example.xls")
    >>> sheet.row += [12, 11, 10]
    >>> sheet.save_as("new_example.xls")
    >>> pe.get_sheet(file_name="new_example.xls")
    pyexcel_sheet1:
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +----------+----------+----------+
    | 1        | 4        | 7        |
    +----------+----------+----------+
    | 2        | 5        | 8        |
    +----------+----------+----------+
    | 3        | 6        | 9        |
    +----------+----------+----------+
    | 12       | 11       | 10       |
    +----------+----------+----------+


Update an existing row to an existing file
-------------------------------------------

Suppose you want to update the last row of the example file as:

    ['N/A', 'N/A', 'N/A']

Here is the sample code::

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_sheet(file_name="example.xls")
    >>> sheet.row[3] = ['N/A', 'N/A', 'N/A']
    >>> sheet.save_as("new_example1.xls")
    >>> pe.get_sheet(file_name="new_example1.xls")
    pyexcel_sheet1:
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +----------+----------+----------+
    | 1        | 4        | 7        |
    +----------+----------+----------+
    | 2        | 5        | 8        |
    +----------+----------+----------+
    | N/A      | N/A      | N/A      |
    +----------+----------+----------+



Add a new column to an existing file
--------------------------------------

And you want to add a column instead:

    ["Column 4", 10, 11, 12]

Here is the code:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_sheet(file_name="example.xls")
    >>> sheet.column += ["Column 4", 10, 11, 12]
    >>> sheet.save_as("new_example2.xls")
    >>> pe.get_sheet(file_name="new_example2.xls")
    pyexcel_sheet1:
    +----------+----------+----------+----------+
    | Column 1 | Column 2 | Column 3 | Column 4 |
    +----------+----------+----------+----------+
    | 1        | 4        | 7        | 10       |
    +----------+----------+----------+----------+
    | 2        | 5        | 8        | 11       |
    +----------+----------+----------+----------+
    | 3        | 6        | 9        | 12       |
    +----------+----------+----------+----------+


Update an existing column to an existing file
-----------------------------------------------

Again let's update "Column 3" with:

   [100, 200, 300]

Here is the sample code:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_sheet(file_name="example.xls")
    >>> sheet.column[2] = ["Column 3", 100, 200, 300]
    >>> sheet.save_as("new_example3.xls")
    >>> pe.get_sheet(file_name="new_example3.xls")
    pyexcel_sheet1:
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +----------+----------+----------+
    | 1        | 4        | 100      |
    +----------+----------+----------+
    | 2        | 5        | 200      |
    +----------+----------+----------+
    | 3        | 6        | 300      |
    +----------+----------+----------+


Alternatively, you could have done like this:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_sheet(file_name="example.xls", name_columns_by_row=0)
    >>> sheet.column["Column 3"] = [100, 200, 300]
    >>> sheet.save_as("new_example4.xls")
    >>> pe.get_sheet(file_name="new_example4.xls")
    pyexcel_sheet1:
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +----------+----------+----------+
    | 1        | 4        | 100      |
    +----------+----------+----------+
    | 2        | 5        | 200      |
    +----------+----------+----------+
    | 3        | 6        | 300      |
    +----------+----------+----------+


How about the same alternative solution to previous row based example? Well, you'd better to have the 
following kind of data

row_example.xls

========= ==== ==== ====
Row 1     1    2    3
Row 2     4    5    6
Row 3     7    8    9
========= ==== ==== ====

.. testcode::
   :hide:

   >>> import os
   >>> import pyexcel
   >>> data = [
   ...      ["Row 1", 1, 2, 3],
   ...      ["Row 2", 4, 5, 6],
   ...      ["Row 3", 7, 8, 9],
   ...  ]
   >>> pyexcel.save_as(array=data, dest_file_name="row_example.xls")

And then you want to update "Row 3" with for example::

    [100, 200, 300]

These code would do the job:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.get_sheet(file_name="row_example.xls", name_rows_by_column=0)
    >>> sheet.row["Row 3"] = [100, 200, 300]
    >>> sheet.save_as("new_example5.xls")
    >>> pe.get_sheet(file_name="new_example5.xls")
    pyexcel_sheet1:
    +-------+-----+-----+-----+
    | Row 1 | 1   | 2   | 3   |
    +-------+-----+-----+-----+
    | Row 2 | 4   | 5   | 6   |
    +-------+-----+-----+-----+
    | Row 3 | 100 | 200 | 300 |
    +-------+-----+-----+-----+


.. testcode::
   :hide:

   >>> os.unlink("new_example.xls")
   >>> os.unlink("new_example1.xls")
   >>> os.unlink("new_example2.xls")
   >>> os.unlink("new_example3.xls")
   >>> os.unlink("new_example4.xls")
   >>> os.unlink("new_example5.xls")
   >>> os.unlink("example.xls")


