.. _formatting:

Sheet: Formatting
===================

Previous section has assumed the data is in the format that you want. In reality, you have to manipulate the data types a bit to suit your needs. Hence, formatters comes into the scene. The formatters take effect when the data is read on the fly. They do not affect the persistence of the data in the excel files. A row or column formatter can be applied to mutilpe rows/columns. There are two ways of applying a formatter:

#. use :meth:`~pyexcel.Sheet.add_formatter`, :meth:`~pyexcel.Sheet.remove_formatter` and :meth:`~pyexcel.Sheet.clear_formatter` to apply formatter on the fly. The formatter takes effect when a cell value is read. In other words, the sheet content is intact until you call :meth:`~pyexcel.Sheet.freeze_formatters` to apply all added formatters.  
#. use :meth:`~pyexcel.Sheet.format` to apply formatter immediately. 


There is slightly different behavior between csv reader and xls reader. The cell type of the cells read by csv reader will be always text while the cell types read by xls reader vary. 


Convert a column of numbers to strings
--------------------------------------

By default, all values in **csv** are read back as texts. However, for xls, xlsx and xlsm files, differnt data type are supported. Numbers are always read as `float`. Therefore, if you should like to have them in string format, you need to do some conversions. Suppose you have the following data in any of the supported excel formats:

======== =========
userid   name
======== =========
10120    Adam     
10121    Bella
10122    Cedar
======== =========

Let's read it out first::

   >>> import pyexcel

.. testcode::
   :hide:

   >>> data = [
   ...     ["userid","name"],
   ...     [10120,"Adam"],  
   ...     [10121,"Bella"],
   ...     [10122,"Cedar"]
   ... ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

.. testcode::
   
   >>> sheet = pyexcel.get_sheet(file_name="example.xls", name_columns_by_row=0)
   >>> sheet.column["userid"]
   [10120.0, 10121.0, 10122.0]

As you can see, `userid` column is of `float` type. Next, let's convert the column to string format::

    >>> sheet.column.format(0, str)
    >>> sheet.column["userid"]
    ['10120.0', '10121.0', '10122.0']

Now, they are in string format.

You can do this row by row as well using :class:`~pyexcel.RowFormatter` or do this to a whote spread sheet using :class:`~pyexcel.SheetFormatter`

.. _cleansing:

Cleanse the cells in a spread sheet
-----------------------------------

Sometimes, the data in a spreadsheet may have unwanted strings in all or some cells. Let's take an example. Suppose we have a spread sheet that contains all strings but it as random spaces before and after the text values. Some field had weird characters, such as "&nbsp;&nbsp;":

================= ============================ ================
        Version        Comments                Author &nbsp;
================= ============================ ================
  v0.0.1          Release versions              &nbsp;Eda
&nbsp; v0.0.2     Useful updates &nbsp; &nbsp;  &nbsp;Freud
================= ============================ ================

.. testcode::
   :hide:

   >>> data = [
   ...     ["        Version", "        Comments", "       Author &nbsp;"],
   ...     ["  v0.0.1       ", " Release versions","           &nbsp;Eda"],
   ...     ["&nbsp; v0.0.2  ", "Useful updates &nbsp; &nbsp;", "  &nbsp;Freud"]
   ... ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

First, let's read the content and see what do we have::

   >>> sheet = pyexcel.get_sheet(file_name="example.xls")

.. testcode::
   :hide:

   >>> sheet.format(lambda v: str(v))

.. testcode::
  
   >>> sheet.to_array()
   [['        Version', '        Comments', '       Author &nbsp;'], ['  v0.0.1       ', ' Release versions', '           &nbsp;Eda'], ['&nbsp; v0.0.2  ', 'Useful updates &nbsp; &nbsp;', '  &nbsp;Freud']]


Now try to create a custom cleanse function::
  
    >>> def cleanse_func(v):
    ...     v = v.replace("&nbsp;", "")
    ...     v = v.rstrip().strip()
    ...     return v
    ...

Then let's create a :class:`~pyexcel.SheetFormatter` and apply it::

    >>> sf = pyexcel.formatters.SheetFormatter(cleanse_func)
    >>> sheet.add_formatter(sf)
    >>> sheet.to_array()
    [['Version', 'Comments', 'Author'], ['v0.0.1', 'Release versions', 'Eda'], ['v0.0.2', 'Useful updates', 'Freud']]

So in the end, you get this:

================= ============================ ================
Version           Comments                     Author
================= ============================ ================
v0.0.1            Release versions             Eda
v0.0.2            Useful updates               Freud
================= ============================ ================

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example.xls")
