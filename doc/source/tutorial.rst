Work with data series
=====================

Suppose you have the following data in any of the supported excel formats:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

Read an excel file
-------------------

You can read it use a SeriesReader::

    >> from pyexcel import SeriesReader
    >> reader = SeriesReader("example_series.ods")

Play with data
---------------

You can get headers::

    >> print reader.series()
    [u'Column 1', u'Column 2', u'Column 3']

You can use a utility function to get all in a dictionary::

    >> from pyexcel.utils import to_dict
    >> data = to_dict(reader)
    >> print data
    {"Column 2": [4, 5, 6], "Column 3": [7, 8, 9], "Column 1": [1, 2, 3]}

Maybe you want to get only the data without the column headers. You can call ``rows()`` instead::

    >> from pyexcel.utils import to_array
    >> data = to_array(reader.rows())
    >> print data
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

You can get data from the bottom to the top one by calling ``rrows()`` instead::

    >> from pyexcel.utils import to_array
    >> data = to_array(reader.rrows())
    >> print data
    [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

You might want the data arranged vertically. You can call ``columns()`` instead::
	
    >> from pyexcel.utils import to_array
    >> data = to_array(reader.columns())
    >> print data
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

You can get columns in reverse sequence as well by calling ``rcolumns()`` instead::
	
    >> from pyexcel.utils import to_array
    >> data = to_array(reader.columns())
    >> print data
    [[7, 8, 9], [4, 5, 6], [1, 2, 3]]

Do you want to flatten the data? you can get the content in one dimensional array. If you are interested in playing with one dimensional enurmation, you can check out these functions ``enumerate()``, ``reverse()``, ``vertical()``, and ``rvertical()``::

    >> data = to_array(reader.enumerate())
    >> print data
    [1, 4, 7, 2, 5, 8, 3, 6, 9]
    >> data = to_array(reader.reverse())
    >> print data
    [9, 6, 3, 8, 5, 2, 7, 4, 1]
    >> data = to_array(reader.vertical())
    >> print data
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >> data = to_array(reader.rvertical())
    >> print data
    [9, 8, 7, 6, 5, 4, 3, 2, 1]

.. note::

    If you do not want to single column headers out from the data body, you may have a look at the ``Reader`` in the next section


Filter out some data
---------------------

You may want to filter odd rows and print them in an array of dictionaries::

    >> from pyexcel.filters import OddRowFilter
    >> reader.filter(OddRowFilter())
    >> data = to_array(reader)
    >> print data
    [{u'Column 1': [2]}, {u'Column 2': [5]}, {u'Column 3': [8]}]

Let's try to further filter out even columns::

    >> from pyexcel.filters import EvenColumnFilter
    >> reader.filter(EvenColumnFilter())
    >> data = to_dict(reader)
    >> print data
    {u'Column 3': [8], u'Column 1': [2]}

Save the data
---------------

Let's save the previous filtered data::

    >> from pyexcel import Writer
    >> w = Writer("example_series_filter.xls")
    >> w.write_reader(reader)
    >> w.close()

When you open `example_series_filter.xls`, you will find these data:

======== ========
Column 1 Column 3
======== ========
2        8
======== ========


The complete code is::

    from pyexcel import SeriesReader, Writer
    from pyexcel.filters import OddRowFilter
    from pyexcel.filters import EvenColumnFilter

    reader = SeriesReader("example_series.ods")
    reader.filter(OddRowFilter())
    reader.filter(EvenColumnFilter)
    writer = Writer("example_series_filter.xls")
    writer.write_reader(reader)
    writer.close()


Work with pure data
===================

Suppose you have the following data in any of the supported excel formats:

== == == ==
1  2  3  4
5  6  7  8
9  10 11 12
== == == ==

Read an excel file
-------------------

You can read it use a SeriesReader::

    >> from pyexcel import Reader
    >> reader = Reader("example_series.xls")

Pay with data
-------------

You can get them in rows or columns::

    >> from pyexcel.utils import to_array
    >> data = to_array(reader.rows())
    >> print data
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    >> from pyexcel.utils import to_array
    >> data = to_array(reader.columns())
    >> print data
    [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

.. note::

   You can explore ``rrows()`` and ``rcolumns()`` too


In the same way, you can get the content in one dimensional array::

    >> data = to_array(reader)
    >> print data
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    >> data = to_array(reader.reverse())
    >> print data
    [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >> data = to_array(reader.vertical())
    >> print data
    [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
    >> data = to_array(reader.rvertical())
    >> print data
    [12,8,4,11,7,3,10,6,2,9,5,1]
