========================================================
pyexcel - Let you focus on data, instead of file formats
========================================================

.. image:: https://api.travis-ci.org/chfw/pyexcel.svg?branch=master
    :target: http://travis-ci.org/chfw/pyexcel

.. image:: https://coveralls.io/repos/chfw/pyexcel/badge.png?branch=master 
    :target: https://coveralls.io/r/chfw/pyexcel?branch=master 

.. image:: https://readthedocs.org/projects/pyexcel/badge/?version=latest
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

================ ========================================================================
Plugins          Supported file formats                                      
================ ========================================================================
pyexcel          csv, csvz, tsv, tsvz                                        
`pyexcel-xls`_   xls, xlsx(r), xlsm(r)
`pyexcel-xlsx`_  xlsx
`pyexcel-ods`_   ods (python 2.6, 2.7 only)                                       
`pyexcel-ods3`_  ods
`pyexcel-text`_  (write only)json, rst, mediawiki,latex, grid, pipe, orgtbl, plain simple
================ ========================================================================

.. _pyexcel-xls: https://github.com/chfw/pyexcel-xls
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

Suppose you want to process the following excel data :

========= ====
Name      Age
========= ====
Adam      28
Beatrice  29
Ceri      30
Dean      26
========= ====

Here are the example code::
   
   >>> import pyexcel as pe
   >>> import pyexcel.ext.xls # import it to handle xls file
   >>> records = pe.get_records(file_name="your_file.xls")
   >>> for record in records:
   ...     print("%s is aged at %d" % (record['Name'], record['Age']))
   Adam is aged at 28
   Beatrice is aged at 29
   Ceri is aged at 30
   Dean is aged at 26


Documentation
=============

Documentation is hosted at `read the docs <https://pyexcel.readthedocs.org/en/latest>`_ and `pyhosted <https://pythonhosted.org/pyexcel/>`_

License
==========

New BSD License

Dependencies
==============

* pyexcel-io >= 0.0.4
* texttable >= 0.8.2

Acknowledgement
===============

All great work have done by odf, ezodf(2), xlrd, xlwt, tabulate and other individual developers. This library unites only the data access code.

Extension management code was copied from `flask <https://github.com/mitsuhiko/flask>`_. 
