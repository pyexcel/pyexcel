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
:Version: |version|


Introduction
-------------

**pyexcel** is a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. This library makes information processing involving excel files an enjoyable task. The data in excel files can be turned into array or dict with least code, vice versa. And ready-made custom filters and formatters can be applied. However, this library is not made for data visualisations. Hence it does not support fonts, colors and charts.

It was created due to the lack of uniform programming interface to access data in different excel formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

In addition, the library recognizes that Excel files are de-facto file format for information sharing in non-software centric organisations. Excel files are not only used for mathematical computation in financial institutions but also used for many other purposes in an office work environment.

All great work have done by individual library developers. This library unites only the data access code. With that said, pyexcel also bring something new on the table. "csvz" and "tsvz" format, new format names as of 2014, are zipped csv or tsv files and supported by pyexcel.

Getting the source
-------------------

Source code is hosted in github. You can get it using git client::

    $ git clone http://github.com/chfw/pyexcel.git

Usage
------

.. testcode::
   :hide:

   >>> import pyexcel
   >>> import pyexcel.ext.xls
   >>> import pyexcel.ext.xlsx
   >>> data = {
   ...     "Sheet 1": [
   ...         [1, 2, 3],
   ...         ["Column 1", "Column 2", "Column 3"],
   ...         [4, 5, 6]
   ...     ],
   ...     "Sheet 2": [
   ...         ["a", "b", "c", "Row 1"],
   ...         ["e", "f", "g", "Row 2"],
   ...         [1, 2, 3, "Row 3"]
   ...     ]
   ... }
   >>> book = pyexcel.Book(data)
   >>> book.save_as("your_file.xls")

Here are the example usages::
   
    >>> import pyexcel as pe
    >>> import pyexcel.ext.xls # import it to be able handle xls file
    >>> import pyexcel.ext.xlsx # xlsx file
    >>> sheet = pe.load("your_file.xls")
    >>> sheet # ascii representation of the content
    Sheet Name: Sheet 1
    +----------+----------+----------+
    | 1        | 2        | 3        |
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +----------+----------+----------+
    | 4        | 5        | 6        |
    +----------+----------+----------+
    >>> sheet["A1"]
    1.0
    >>> # format a row using a lambda function
    >>> sheet.row.format(1, str, lambda value: str(value))
    >>> sheet.column[0]
    [1.0, 'Column 1', 4.0]
    >>> sheet.row[2]
    [4.0, 5.0, 6.0]
    >>> sheet.name_columns_by_row(1)
    >>> sheet.column["Column 1"]
    [1.0, 4.0]
    >>> sheet.save_as("myfile.csv")
    >>> # load the whole excel file
    >>> book = pe.load_book("your_file.xls")
    >>> book
    Sheet Name: Sheet 1
    +----------+----------+----------+
    | 1        | 2        | 3        |
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +----------+----------+----------+
    | 4        | 5        | 6        |
    +----------+----------+----------+
    Sheet Name: Sheet 2
    +---+---+---+-------+
    | a | b | c | Row 1 |
    +---+---+---+-------+
    | e | f | g | Row 2 |
    +---+---+---+-------+
    | 1 | 2 | 3 | Row 3 |
    +---+---+---+-------+
    >>> # alternative access to the same cell on sheet 1
    >>> print(book["Sheet 1"][0,0])
    1.0
    >>> book["Sheet 2"].name_rows_by_column(3)
    >>> book["Sheet 2"].row["Row 3"]
    [1.0, 2.0, 3.0]
    >>> book.save_as("new_file.xlsx") # save a copy

.. testcode::
   :hide:
   
   >>> import os
   >>> os.unlink("your_file.xls")
   >>> os.unlink("myfile.csv")
   >>> os.unlink("new_file.xlsx")


Installation
-------------

You can install it via pip::

    $ pip install pyexcel

For individual excel file formats, please install them as you wish:

================ ============================================================ ============= ======================== =============================	
Plugins          Supported file formats                                       Dependencies  Python versions			 Comments						
================ ============================================================ ============= ======================== =============================	
pyexcel          csv, csvz [#f1]_, tsv, tsvz [#f2]_                                         2.6, 2.7, 3.3, 3.4, pypy 								
`pyexcel-xls`_   xls, xlsx(read only), xlsm(read only)                        xlrd, xlwt    2.6, 2.7, 3.3, 3.4, pypy only support writing xls
`pyexcel-xlsx`_  xlsx,                                                        openpyxl      2.6, 2.7, 3.3, 3.4, pypy 								
`pyexcel-ods`_   ods (python 2.6, 2.7)                                        odfpy         2.6, 2.7				 								
`pyexcel-ods3`_  ods (python 2.7, 3.3, 3.4)                                   ezodf, lxml   3.3, 3.4				 								
`pyexcel-text`_  json, rst, mediawiki,latex, grid, pipe, orgtbl, plain simple tabulate      2.6, 2.7, 3.3, 3.4, pypy only support writing to files	
================ ============================================================ ============= ======================== =============================

.. _pyexcel-xls: https://github.com/chfw/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/chfw/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/chfw/pyexcel-ods
.. _pyexcel-ods3: https://github.com/chfw/pyexcel-ods3
.. _pyexcel-text: https://github.com/chfw/pyexcel-text


Please import them before you start to access the desired file formats::

    from pyexcel.ext import extension_name

or::

    import pyexcel.ext.extension_name

.. table:: Plugin compatibility table

    ======= ======= ======= ======== ====== ======
    pyexcel xls     xlsx    ods      ods3   text  
    ======= ======= ======= ======== ====== ======
    v0.0.9  0.0.1+  0.0.1+  0.0.2+   0.0.2+ 0.0.2+
    v0.0.8  0.0.1   n/a     0.0.2    0.0.2  0.0.1 
    v0.0.7  n/a             0.0.2    0.0.2  n/a    
    v0.0.6                  0.0.2    0.0.2      
    ======= ======= ======= ======== ====== ======

More usage examples
--------------------

Tutorial
+++++++++

.. toctree::

   tutorial
   tutorial05
   tutorial02
   tutorial03
   tutorial04
   tutorial06

Cook book
++++++++++

.. toctree::

   cookbook

Real world cases
+++++++++++++++++++

.. toctree::

   answers

API documentation
------------------

.. toctree::
   :maxdepth: 2

   api
   iapi


Developer's guide
------------------

.. toctree::

   guide

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file
