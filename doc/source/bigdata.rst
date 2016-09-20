================================================================================
Work with big data sheet
================================================================================

When you are dealing with huge amount of data, e.g. 64GB, obviously you would not
like to fill up your memory with those data. Hence pagnation feature is developed
to read partial data into memory for processing. You can pagninate by row, by
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
   ...     start_row=2, row_limit=3)
   ...     start_column=1, column_limit=2)
   your_file.csv:
   +---+----+----+
   | 3 | 23 | 33 |
   +---+----+----+
   | 4 | 24 | 34 |
   +---+----+----+
   | 5 | 25 | 35 |
   +---+----+----+


The pagination support is available across all pyexcel plugins.

.. note::

   No column pagination support for query sets as data source. 
