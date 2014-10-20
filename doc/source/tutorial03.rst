Formatting cells
================

Previous section has assumed the data is in the format that you want. In reality, you have to manipulate the data types a bit to suit your needs. Hence, `formatters` comes into the scene. The formatters take effect when the data is read on the fly. They do not affect the persistence of the data in the excel files.

Convert a column of numbers to strings
--------------------------------------

By default, `pyexcel` will render numbers into numbers. For csv file, intergers are read as `int` and float numbers are read as `float`. However, for xls, xlsx and xlsm files, numbers are always read as `float`. Therefore, if you should like to have them in string format, you need to do some conversions. Suppose you have the following data in any of the supported excel formats:

======== =========
userid   name
======== =========
10120    Adam     
10121    Bella
10122    Cedar
======== =========

Let's read it out first::

    >> from pyexcel import SeriesReader
    >> reader = SeriesReader("example.xls")
    >> from pyexcel.utils import to_dict
    >> to_dict(reader)
    {u'userid': [10120.0, 10121.0, 10122.0], u'name': [u'Adam', u'Bella', u'Cedar']}

As you can see, `userid` column is of `float` type. Next, let's convert the column to string format::

    >> from pyexcel.formatters import ColumnFormatter, STRING_FORMAT
    >> formatter = ColumnFormatter(0, STRING_FORMAT)
    >> reader.add_formatter(formatter)
    >> to_dict(reader)
    {u'userid': ['10120.0', '10121.0', '10122.0'], u'name': [u'Adam', u'Bella', u'Cedar']}

Now, they are in string format.

You can do this row by row as well using `RowFormatter` or do this to a whote spread sheet using `SheetFormatter`

Cleanse the cells in a spread sheet
-----------------------------------

Sometimes, the data in a spreadsheet may have unwanted strings in all or some cells. Let's take an example. Suppose we have a spread sheet that contains all strings but it as random spaces before and after the text values. Some field had weird characters, such as "&nbsp;&nbsp;":

================= ============================ ================
        Version        Comments                Author &nbsp;
================= ============================ ================
  v0.0.1          Release versions              &nbsp;Eda
&nbsp; v0.0.2     Useful updates &nbsp; &nbsp;  &nbsp;Freud
================= ============================ ================

First, let's read the content and see what do we have::

    >>> from pyexcel import Reader
    >>> from pyexcel.utils import to_array
    >>> r=Reader("tutorial_datatype_02.ods")
    >>> to_array(r)
    [[u'Version', u'Comments', u'Author &nbsp;'], [u'v0.0.1 ', u'Release versions',
    u'&nbsp;Eda'], [u'&nbsp; V0.02 ', u'Useful updates &nbsp; &nbsp;', u'&nbsp;Freud
    ']]


Now try to create a custom cleanse function::
  
    >>> def cleanse_func(v, t):
    ...     v = v.replace("&nbsp;", "")
    ...     v = v.rstrip().strip()
    ...     return v
    ...

Then let's create a `SheetFormatter` and apply it::

    >>> from pyexcel.formatters import SheetFormatter
    >>> from pyexcel.formatters import STRING_FORMAT
    >>> sf = SheetFormatter(STRING_FORMAT, cleanse_func)
    >>> r.add_formatter(sf)
    >>> to_array(r)
    [[u'Version', u'Comments', u'Author'], [u'v0.0.1', u'Release versions', u'Eda'],
     [u'V0.02', u'Useful updates', u'Freud']]

So in the end, you get this:

================= ============================ ================
        Version        Comments                Author
================= ============================ ================
v0.0.1            Release versions             Eda
v0.0.2            Useful updates               Freud
================= ============================ ================
