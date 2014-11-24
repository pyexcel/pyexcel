========================================================
pyexcel - Let you focus on data, instead of file formats
========================================================

.. image:: https://api.travis-ci.org/chfw/pyexcel.svg?branch=master
    :target: http://travis-ci.org/chfw/pyexcel

.. image:: https://coveralls.io/repos/chfw/pyexcel/badge.png?branch=master 
    :target: https://coveralls.io/r/chfw/pyexcel?branch=master 

.. image:: https://readthedocs.org/projects/pyexcel/badge/?version=latest
    :target: https://readthedocs.org/projects/pyexcel/?badge=latest

.. image:: https://pypip.in/d/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

.. image:: https://pypip.in/py_versions/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

.. image:: https://pypip.in/implementation/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel
    :alt: Supported Python implementation

**pyexcel** and its plugins are a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. Its mission is to let you focus on data itself and it deals with different file formats. Fonts, colors and charts are not supported.

All great work have done by odf, ezodf(2), xlrd, xlwt, tabulate and other individual developers. This library unites only the data access code.

Usage Exmaples::

    >>> import pyexcel as pe
    >>> import pyexcel.ext.xl # import it to be able handle xls, xlsx, xlsm files
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


Documentation
=============

Latest document is hosted at `pyexcel@read the docs <https://pyexcel.readthedocs.org/en/latest>`_ and latest stable version is hosted in `pyexcel@pyhosted <https://pythonhosted.org/pyexcel/>`_

Latest stable
=============

0.0.7

Installation
============
You can install it via pip::

    $ pip install pyexcel


or clone it and install it::

    $ git clone http://github.com/chfw/pyexcel.git
    $ cd pyexcel
    $ python setup.py install

Installation of individual plugins , please refer to individual plugin page.

================ ============================================================ =============================
Plugins          Supported file formats                                       Comments
================ ============================================================ =============================
pyexcel          csv, csvz, tsv, tsvz                                              
`pyexcel-xl`_    xls, xlsx, xlsm                                              
`pyexcel-ods`_   ods (python 2.6, 2.7)                                        
`pyexcel-ods3`_  ods (python 2.7, 3.3, 3.4)                                   
`pyexcel-text`_  json, rst, mediawiki,latex, grid, pipe, orgtbl, plain simple only support writing to files
================ ============================================================ =============================

.. _pyexcel-xl: https://github.com/chfw/pyexcel-xl
.. _pyexcel-ods: https://github.com/chfw/pyexcel-ods
.. _pyexcel-ods3: https://github.com/chfw/pyexcel-ods3
.. _pyexcel-text: https://github.com/chfw/pyexcel-text

Plugin compatibility 
-------------------------------
======= ======= ======== ====== ======
pyexcel xl      ods      ods3	text  
======= ======= ======== ======	======
v0.0.8	0.0.1   0.0.2	 0.0.2	0.0.1 
v0.0.7	n/a     0.0.2	 0.0.2	n/a    
v0.0.6          0.0.2    0.0.2	    
v0.0.5          0.0.1    0.0.1     		   
v0.0.4          0.0.1    0.0.1	    
v0.0.3          n/a      n/a    
======= ======= ======== ======	======

Test 
=====

Here is the test command::

    pip install -r tests/requirements.txt
    make test

On Windows, please use::

    test.bat

For more local test coverage, you can add `--cover-html --cover-html-dir=your_file_directory` to `test.sh` or `test.bat`


Known Issues
=============

* If a zero was typed in a DATE formatted field in xls, you will get "01/01/1900".
* If a zero was typed in a TIME formatted field in xls, you will get "00:00:00".

Acknowledgement
===============

Extension management code was copied from `flask <https://github.com/mitsuhiko/flask>`_. 
