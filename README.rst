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

.. _file-format-list:

.. table:: A list of file formats supported by external plugins

   ================= ========================================
   Plugins           Supported file formats
   ================= ========================================
   `pyexcel-xls`_    xls, xlsx(read only), xlsm(read only)
   `pyexcel-xlsx`_   xlsx
   `pyexcel-xlsxw`_  xlsx(write only)
   `pyexcel-ods3`_   ods (python 2.6, 2.7, 3.3, 3.4)
   `pyexcel-ods`_    ods (python 2.6, 2.7)
   `pyexcel-text`_   (write only)json, rst, mediawiki, html
                     latex, grid, pipe, orgtbl, plain simple
   ================ ========================================

.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text
.. _xlsx: https://github.com/pyexcel/pyexcel-xlsxw
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

.. code-block:: python

    >>> import pyexcel
    >>> content = "1,2,3\n3,4,5"
    >>> sheet = pyexcel.Sheet()
    >>> sheet.csv = content
    >>> sheet.array
    [[1, 2, 3], [3, 4, 5]]
    >>> with open("myfile.xlsx", "wb") as output:
    ...     write_count_not_used = output.write(sheet.xlsx)

.. testcode::
   :hide:

    >>> import os
	>>> os.unlink("myfile.xlsx")

Development guide
================================================================================

Development steps for code changes

#. git clone https://github.com/pyexcel/pyexcel.git
#. cd pyexcel

Upgrade your setup tools and pip. They are needed for development and testing only:

#. pip install --upgrade setuptools "pip==7.1"

Then install relevant development requirements:

#. pip install -r rnd_requirements.txt # if such a file exists
#. pip install -r requirements.txt
#. pip install -r tests/requirements.txt


In order to update test environment, and documentation, additional setps are
required:

#. pip install moban
#. git clone https://github.com/pyexcel/pyexcel-commons.git
#. make your changes in `.moban.d` directory, then issue command `moban`

What is rnd_requirements.txt
-------------------------------

Usually, it is created when a dependent library is not released. Once the dependecy is installed(will be released), the future version of the dependency in the requirements.txt will be valid.

What is pyexcel-commons
---------------------------------

Many information that are shared across pyexcel projects, such as: this developer guide, license info, etc. are stored in `pyexcel-commons` project.

What is .moban.d
---------------------------------

`.moban.d` stores the specific meta data for the library.

How to test your contribution
------------------------------

Although `nose` and `doctest` are both used in code testing, it is adviable that unit tests are put in tests. `doctest` is incorporated only to make sure the code examples in documentation remain valid across different development releases.

On Linux/Unix systems, please launch your tests like this::

    $ make test

On Windows systems, please issue this command::

    > test.bat

License
================================================================================

New BSD License


Acknowledgement
===============

All great work have done by odf, ezodf(2), xlrd, xlwt, tabulate and other individual developers. This library unites only the data access code.

