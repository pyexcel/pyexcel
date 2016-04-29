========================================================
pyexcel - Let you focus on data, instead of file formats
========================================================

.. image:: https://api.travis-ci.org/pyexcel/pyexcel.svg?branch=master
    :target: http://travis-ci.org/pyexcel/pyexcel

.. image:: https://codecov.io/github/pyexcel/pyexcel/coverage.svg?branch=master
    :target: https://codecov.io/github/pyexcel/pyexcel?branch=master

.. image:: https://readthedocs.org/projects/pyexcel/badge/?verssion=latest
    :target: http://pyexcel.readthedocs.org/en/latest/


Known constraints
==================

Fonts, colors and charts are not supported. 


Feature Highlights
===================

1. One API to handle multiple data sources:

   * physical file
   * memory file
   * SQLAlchemy table
   * Django Model
   * Python data stuctures: dictionary, records and array
2. One application programming interface(API) to read and write data in various excel file formats.


Available Plugins
=================

================ ========================================
Plugins          Supported file formats                  
================ ========================================
`pyexcel-io`_    csv, csvz, tsv, tsvz
`pyexcel-xls`_   xls, xlsx(r), xlsm(r)
`pyexcel-xlsx`_  xlsx
`pyexcel-ods`_   ods (python 2.6, 2.7 only)              
`pyexcel-ods3`_  ods
`pyexcel-text`_  (write only)json, rst, mediawiki,latex,
                 grid, pipe, orgtbl, plain simple
================ ========================================

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text

Installation
============

You can install it via pip:

.. code-block:: bash

    $ pip install pyexcel


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/pyexcel/pyexcel.git
    $ cd pyexcel
    $ python setup.py install

Installation of individual plugins , please refer to individual plugin page.

Usage
===============


JSON
------------------

.. code-block:: python
   
    >>> import pyexcel as pe
    >>> an_array = [[1,2]]
    >>> sheet = pe.Sheet(an_array)
    >>> sheet.json
    '{"pyexcel": [[1, 2]]}'

Note: It is available with pyexcel v0.2.1 and pyexcel-text 0.2.0

HTML
---------------------

.. code-block:: python

    >>> sheet.html # doctest: +ELLIPSIS
    ...'Sheet Name: pyexcel\n<table>\n<tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td></tr>\n</table>\n'

Note: It is available with pyexcel v0.2.1 and pyexcel-text 0.2.0

TSV
---------------------

.. code-block:: python

    >>> sheet.tsv
    '1\t2\r\n'

Note: TSV and the rest of the formats are available with pyexcel v0.2.2 and its plugins at version 0.2.0+ only

CSV
---------------------

.. code-block:: python

    >>> sheet.csv
    '1,2\r\n'


XLS
----------------------

.. code-block:: python

    >>> sheet.xls # doctest: +ELLIPSIS
    '\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00\x00...\x00\x00\x00\x00\x00\x00'
	
XLSX
----------------------

.. code-block:: python

    >>> sheet.xlsx # doctest: +ELLIPSIS
    ...'PK\x03\x04\x14\x00\x00\x00\x08...\x11\x00\x00\x00\x00'
	
ODS
----------------------

.. code-block:: python

    >>> sheet.ods # doctest: +ELLIPSIS
    ...'PK\x03\x04\x14\x00\x00\x00\x00...\x07\x00\x00\x00\x00'

Compressed csv (csvz)
----------------------

.. code-block:: python

    >>> sheet.csvz # doctest: +ELLIPSIS
    ...'PK\x03\x04\x14\x00\x00\x00\x00...x00\x00\x00\x00'


Documentation
=============

Documentation is hosted at `read the docs <https://pyexcel.readthedocs.org/en/latest>`_ and `pyhosted <https://pythonhosted.org/pyexcel/>`_


License
================================================================================

New BSD License


Acknowledgement
===============

All great work have done by odf, ezodf(2), xlrd, xlwt, tabulate and other individual developers. This library unites only the data access code.

Extension management code was reused from `flask <https://github.com/mitsuhiko/flask>`_. 
