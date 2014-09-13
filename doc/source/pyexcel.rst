.. pyexcel documentation master file, created by
   sphinx-quickstart on Tue Sep  9 08:53:12 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`pyexcel` - Let you focus on data, instead of file formats
==========================================================

:Author: C.W.
:Source code: http://github.com/chfw/pyexcel
:Issues: http://github.com/chfw/pyexcel/issues
:License: GPL v3
:Version: |release|

Introduction
-------------

**pyexcel** is a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. It does not support styling, charts.

It was created due to the lack of uniform programming interface to access data in different formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

All great work have done by odf, xlrd and other individual developers. This library unites only the data access code.


Installation
-------------

You can install it via pip::

    $ pip install pyexcel


Getting the source
-------------------

Source code is hosted in github. You can get it using git client::

    $ git clone http://github.com/chfw/pyexcel.git


Tutorial
-------------

Read an excel file
^^^^^^^^^^^^^^^^^^^
Suppose you have the following data in any of the supported excel formats:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

You can read it use a SeriesReader::

    >> from pyexcel import SeriesReader
    >> reader = SeriesReader("example_series.ods")

Get data in different ways
^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

You might want the data arranged vertically. You can call ``columns()`` instead::
	
    >> from pyexcel.utils import to_array
    >> data = to_array(reader.columns())
    >> print data
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

Filter out some data
^^^^^^^^^^^^^^^^^^^^^

You may want to filter odd rows and print them in an array of dictionaries::

    >> from pyexcel.filters import OddRowFilter
    >> reader.filter(OddRowFilter())
    >> data = to_array(reader)
    >> print data
    [{u'Column 1': [2]}, {u'Column 2': [5]}, {u'Column 3': [8]}]

Let's try to further filter out even columns::

    >> from pyexcel.filters import EvenColumnFilter
    >> reader.filter(EvenColumnFilter)
    >> data = to_dict(reader)
    >> print data
    {u'Column 3': [8], u'Column 1': [2]}

Save the data
^^^^^^^^^^^^^^

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

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

