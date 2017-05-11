================================================================================
Work with big data sheet
================================================================================


Pagination
--------------------------------------------------------------------------------

When you are dealing with huge amount of data, e.g. 64GB, obviously you would not
like to fill up your memory with those data. Hence pagination feature is developed
to read partial data into memory for processing. You can paginate by row, by
column and by both.

.. testcode::
   :hide:

    >>> import sys
    >>> if sys.version_info[0] < 3:
    ...     from StringIO import StringIO
    ... else:
    ...     from io import StringIO
    >>> from pyexcel_io._compact import OrderedDict

Let's assume the following file is a huge csv file:

.. code-block:: python

   >>> import datetime
   >>> import pyexcel as pe
   >>> data = [
   ...     [1, 21, 31],
   ...     [2, 22, 32],
   ...     [3, 23, 33],
   ...     [4, 24, 34],
   ...     [5, 25, 35],
   ...     [6, 26, 36]
   ... ]
   >>> pe.save_as(array=data, dest_file_name="your_file.csv")

And let's pretend to read partial data:

.. code-block:: python

   >>> pe.get_sheet(file_name="your_file.csv", start_row=2, row_limit=3)
   your_file.csv:
   +---+----+----+
   | 3 | 23 | 33 |
   +---+----+----+
   | 4 | 24 | 34 |
   +---+----+----+
   | 5 | 25 | 35 |
   +---+----+----+

And you could as well do the same for columns:

.. code-block:: python

   >>> pe.get_sheet(file_name="your_file.csv", start_column=1, column_limit=2)
   your_file.csv:
   +----+----+
   | 21 | 31 |
   +----+----+
   | 22 | 32 |
   +----+----+
   | 23 | 33 |
   +----+----+
   | 24 | 34 |
   +----+----+
   | 25 | 35 |
   +----+----+
   | 26 | 36 |
   +----+----+

Obvious, you could do both at the same time:

.. code-block:: python

   >>> pe.get_sheet(file_name="your_file.csv",
   ...     start_row=2, row_limit=3,
   ...     start_column=1, column_limit=2)
   your_file.csv:
   +----+----+
   | 23 | 33 |
   +----+----+
   | 24 | 34 |
   +----+----+
   | 25 | 35 |
   +----+----+


The pagination support is available across all pyexcel plugins.

.. note::

   No column pagination support for query sets as data source. 


Formatting while transcoding a big data file
--------------------------------------------------------------------------------

If you are transcoding a big data set, conventional formatting method would not
help unless a on-demand free RAM is available. However, there is a way to minimize
the memory footprint of pyexcel while the formatting is performed.

Let's continue from previous example. Suppose we want to transcode "your_file.csv"
to "your_file.xls" but increase each element by 1.

What we can do is to define a row renderer function as the following:

   >>> def increment_by_one(row):
   ...     for element in row:
   ...         yield element + 1

Then pass it onto save_as function using row_renderer:

   >>> pe.isave_as(file_name="your_file.csv",
   ...             row_renderer=increment_by_one,
   ...             dest_file_name="your_file.xlsx")


.. note::

   If the data content is from a generator, isave_as has to be used.
   
We can verify if it was done correctly:

   >>> pe.get_sheet(file_name="your_file.xlsx")
   your_file.csv:
   +---+----+----+
   | 2 | 22 | 32 |
   +---+----+----+
   | 3 | 23 | 33 |
   +---+----+----+
   | 4 | 24 | 34 |
   +---+----+----+
   | 5 | 25 | 35 |
   +---+----+----+
   | 6 | 26 | 36 |
   +---+----+----+
   | 7 | 27 | 37 |
   +---+----+----+

.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("your_file.csv")
    >>> os.unlink("your_file.xlsx")
