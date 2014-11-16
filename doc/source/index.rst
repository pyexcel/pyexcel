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

**pyexcel** is a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. The data in excel files can be turned into array or dict with least code, and vice versa. And ready-made or custom filters and formatters can be applied. But it does not support fonts, colors and charts.

It was created due to the lack of uniform programming interface to access data in different excel formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

In addition, the library recognizes that Excel files are de-facto file format for information sharing in non-software centric organisations. Excel files are not only used for mathematical computation in financial institutions but also used for many other purposes in an office work environment.

All great work have done by odf, xlrd and other individual developers. This library unites only the data access code.

.. testcode::
   :hide:

   >>> import pyexcel
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

Usage
=====

    >>> import pyexcel as pe
    >>> sheet = pe.load("your_file.xls")
    >>> sheet
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


Getting the source
-------------------

Source code is hosted in github. You can get it using git client::

    $ git clone http://github.com/chfw/pyexcel.git


Open Document Spreadsheet(ods) Support
-----------------------------------------

In order to add ods support, please choose one of two packages: `pyexcel-ods <https://github.com/chfw/pyexcel-ods>`__ or `pyexcel-ods3 <https://github.com/chfw/pyexcel-ods3>`__ . Please read individual installation instructions respectively. Here is the comparsion of two packages:

============ ========== ========== ========== ========== ==============
package      python 2.6 python 2.7 python 3.3 python 3.4 lxml dependent
============ ========== ========== ========== ========== ==============
pyexcel-ods  yes	    yes	   	   						 no   		  
pyexcel-ods3 		    yes        yes        yes		 yes		   	 		   
============ ========== ========== ========== ========== ============== 


Plugin compatibility management
-------------------------------
======= ======== ====== 
pyexcel ods      ods3
======= ======== ======
v0.0.8
v0.0.7
v0.0.6  0.0.2    0.0.2
v0.0.5                  		   
v0.0.4  0.0.1    0.0.1
v0.0.3                  		   
v0.0.2	                	   
v0.0.1  n/a      n/a
======= ======== ======

Usage examples
----------------

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

API documentation
++++++++++++++++++

.. toctree::

    api
    iapi

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

