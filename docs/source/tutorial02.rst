
Sheet: Data filtering
======================

use :meth:`~pyexcel.Sheet.filter` function to apply a filter immediately. The content is modified.


Suppose you have the following data in any of the supported excel formats:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

    >>> import pyexcel

.. testcode::
   :hide:

   >>> import os
   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 2, 3],
   ...      [4, 5, 6],
   ...      [7, 8, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example_series.xls")

.. code-block:: python

    >>> sheet = pyexcel.get_sheet(file_name="example_series.xls", name_columns_by_row=0)
    >>> sheet.content
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 1        | 2        | 3        |
    +----------+----------+----------+
    | 4        | 5        | 6        |
    +----------+----------+----------+
    | 7        | 8        | 9        |
    +----------+----------+----------+

Filter out some data
--------------------------

You may want to filter odd rows and print them in an array of dictionaries:

.. code-block:: python

    >>> sheet.filter(row_indices=[0, 2])
    >>> sheet.content
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 4        | 5        | 6        |
    +----------+----------+----------+

Let's try to further filter out even columns:

.. code-block:: python

    >>> sheet.filter(column_indices=[1])
    >>> sheet.content
    +----------+----------+
    | Column 1 | Column 3 |
    +==========+==========+
    | 4        | 6        |
    +----------+----------+

Save the data
*************

Let's save the previous filtered data:

.. code-block:: python

    >>> sheet.save_as("example_series_filter.xls")

When you open `example_series_filter.xls`, you will find these data

======== ========
Column 1 Column 3
======== ========
2        8
======== ========

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example_series_filter.xls")


How to filter out empty rows in my sheet?
**************************************************

Suppose you have the following data in a sheet and you want to remove those rows with blanks:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.Sheet([[1,2,3],['','',''],['','',''],[1,2,3]])

You can use :class:`pyexcel.filters.RowValueFilter`, which examines each row, return `True` if the row should be filtered out. So, let's define a filter function:

.. code-block:: python

    >>> def filter_row(row_index, row):
    ...     result = [element for element in row if element != '']
    ...     return len(result)==0


And then apply the filter on the sheet:

.. code-block:: python

    >>> del sheet.row[filter_row]
    >>> sheet
    pyexcel sheet:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+

   

.. testcode::
   :hide:

   >>> os.unlink("example_series.xls")
