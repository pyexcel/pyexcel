Filtering cells
================

There are three ways of applying a filter:

#. use `add_filter`, `remove_filter` and `clear_filter` to interactively apply a filter. The content is not modified until you call `freeze_filters`
#. use `filter` function to apply a filter immediately. The content is modified.

Work with data series in a single sheet
---------------------------------------

Suppose you have the following data in any of the supported excel formats:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

Read an excel file
******************

You can read it use a SeriesReader::

    >>> import pyexcel

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

.. testcode::

   >>> sheet = pyexcel.load("example_series.xls", name_columns_by_row=0)

.. testcode::
   :hide:
   >>> sheet._column_names = [ str(name) for name in sheet._column_names]

Play with data
**************

You can get headers::

    >>> print(list(sheet.colnames))
    ['Column 1', 'Column 2', 'Column 3']

You can use a utility function to get all in a dictionary::

    >>> sheet.to_dict()
    OrderedDict([('Column 1', [1.0, 4.0, 7.0]), ('Column 2', [2.0, 5.0, 8.0]), ('Column 3', [3.0, 6.0, 9.0])])

Maybe you want to get only the data without the column headers. You can call ``rows()`` instead::

    >>> pyexcel.to_array(sheet.rows())
    [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

You can get data from the bottom to the top one by calling ``rrows()`` instead::

    >>> pyexcel.utils.to_array(sheet.rrows())
    [[7.0, 8.0, 9.0], [4.0, 5.0, 6.0], [1.0, 2.0, 3.0]]

You might want the data arranged vertically. You can call ``columns()`` instead::
	
    >>> pyexcel.utils.to_array(sheet.columns())
    [[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]

You can get columns in reverse sequence as well by calling ``rcolumns()`` instead::
	
    >>> pyexcel.utils.to_array(sheet.rcolumns())
    [[3.0, 6.0, 9.0], [2.0, 5.0, 8.0], [1.0, 4.0, 7.0]]

Do you want to flatten the data? you can get the content in one dimensional array. If you are interested in playing with one dimensional enurmation, you can check out these functions ``enumerate()``, ``reverse()``, ``vertical()``, and ``rvertical()``::

    >>> pyexcel.to_array(sheet.enumerate())
    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    >>> pyexcel.to_array(sheet.reverse())
    [9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]
    >>> pyexcel.to_array(sheet.vertical())
    [1.0, 4.0, 7.0, 2.0, 5.0, 8.0, 3.0, 6.0, 9.0]
    >>> pyexcel.to_array(sheet.rvertical())
    [9.0, 6.0, 3.0, 8.0, 5.0, 2.0, 7.0, 4.0, 1.0]

.. note::

    If you do not want to single column headers out from the data body, you may have a look at the ``Reader`` in the next section


Filter out some data
********************

You may want to filter odd rows and print them in an array of dictionaries::

    >>> sheet.add_filter(pyexcel.OddRowFilter())
    >>> sheet.to_array()
    [['Column 1', 'Column 2', 'Column 3'], [4.0, 5.0, 6.0]]

Let's try to further filter out even columns::

    >>> sheet.add_filter(pyexcel.EvenColumnFilter())
    >>> sheet.to_dict()
    OrderedDict([('Column 1', [4.0]), ('Column 3', [6.0])])

Save the data
*************

Let's save the previous filtered data::

    >>> sheet.save_as("example_series_filter.xls")

When you open `example_series_filter.xls`, you will find these data

======== ========
Column 1 Column 3
======== ========
2        8
======== ========


The complete code is::

    import pyexcel

    sheet = pyexcel.load("example_series.xls")
    sheet.add_filter(pyexcel.OddRowFilter())
    sheet.add_filter(pyexcel.EvenColumnFilter())
    sheet.save_as("example_series_filter.xls")


.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example_series_filter.xls")
	

Work with multi-sheet file
--------------------------

How do I read a book, pocess it and save to a new book
******************************************************

Yes, you can do that. The code looks like this::

   import pyexcel

   book = pyexcel.load("yourfile.xls")
   for sheet in book:
       # do you processing with sheet
       # do filtering?
       pass
   book.save_as("output.xls")
 
What would happen if I save a multi sheet book into "csv" file
**************************************************************

Well, you will get one csv file per each sheet. Suppose you have these code::

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

You will end up with three csv files::

   >>> import glob
   >>> outputfiles = glob.glob("myfile_*.csv")
   >>> for file in sorted(outputfiles):
   ...     print(file)
   ...
   myfile_Sheet 1.csv
   myfile_Sheet 2.csv
   myfile_Sheet 3.csv

and their content is the value of the dictionary at the corresponding key

.. testcode::
   :hide:

   >>> os.unlink("myfile_Sheet 1.csv")
   >>> os.unlink("myfile_Sheet 2.csv")
   >>> os.unlink("myfile_Sheet 3.csv")
