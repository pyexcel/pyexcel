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
   ...         [4, 5, 6]
   ...     ],
   ...     "Sheet 2": [
   ...         ["a", "b", "c"],
   ...         ["e", "f", "g"]
   ...     ]
   ... }
   >>> book = pyexcel.Book(data)
   >>> book.save_as("your_file.xls")

Usage
=====

    >>> import pyexcel as pe
    >>> book = pe.load_book("your_file.xls")
    >>> book
    Sheet Name: Sheet 1
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet Name: Sheet 2
    +---+---+---+
    | a | b | c |
    +---+---+---+
    | e | f | g |
    +---+---+---+
    >>> # access first sheet's top left cell
    >>> print(book["Sheet 1"]["A1"])
    1.0
    >>> # alternative access to the same cell
    >>> print(book["Sheet 1"][0,0])
    1.0

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

