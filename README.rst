========================================================
pyexcel - Let you focus on data, instead of file formats
========================================================

.. image:: https://api.travis-ci.org/chfw/pyexcel.svg?branch=master
    :target: http://travis-ci.org/chfw/pyexcel

.. image:: https://coveralls.io/repos/chfw/pyexcel/badge.png?branch=master 
    :target: https://coveralls.io/r/chfw/pyexcel?branch=master 

.. image:: https://readthedocs.org/projects/pyexcel/badge/?version=latest
    :target: https://readthedocs.org/projects/pyexcel/?badge=latest

.. image:: https://pypip.in/version/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

.. image:: https://pypip.in/d/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

.. image:: https://pypip.in/py_versions/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

Known constraints
==================

Fonts, colors and charts are not supported. 


Available Plugins
=================

================ ============================================================
Plugins          Supported file formats                                      
================ ============================================================
pyexcel          csv, csvz, tsv, tsvz                                        
`pyexcel-xl`_    xls, xlsx(r), xlsm(r)
`pyexcel-xlsx`_  xlsx
`pyexcel-ods`_   ods (python 2.6, 2.7)                                       
`pyexcel-ods3`_  ods (python 2.7, 3.3, 3.4)                                  
`pyexcel-text`_  json, rst, mediawiki,latex, grid, pipe, orgtbl, plain simple
================ ============================================================

.. _pyexcel-xl: https://github.com/chfw/pyexcel-xl
.. _pyexcel-xlsx: https://github.com/chfw/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/chfw/pyexcel-ods
.. _pyexcel-ods3: https://github.com/chfw/pyexcel-ods3
.. _pyexcel-text: https://github.com/chfw/pyexcel-text

Installation
============
You can install it via pip::

    $ pip install pyexcel


or clone it and install it::

    $ git clone http://github.com/chfw/pyexcel.git
    $ cd pyexcel
    $ python setup.py install

Installation of individual plugins , please refer to individual plugin page.

Usage
===============

Here are some example codes::

    >>> import pyexcel as pe
    >>> import pyexcel.ext.xl # import it to be able handle xls file
    >>> import pyexcel.ext.xlsx # import it to be able handle xlsx file
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

Documentation is hosted at `read the docs <https://pyexcel.readthedocs.org/en/latest>`_ and `pyhosted <https://pythonhosted.org/pyexcel/>`_

Known Issues
=============

* If a zero was typed in a DATE formatted field in xls, you will get "01/01/1900".
* If a zero was typed in a TIME formatted field in xls, you will get "00:00:00".

Acknowledgement
===============

All great work have done by odf, ezodf(2), xlrd, xlwt, tabulate and other individual developers. This library unites only the data access code.

