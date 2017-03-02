.. pyexcel documentation master file, created by
   sphinx-quickstart on Tue Sep  9 08:53:12 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`pyexcel` - Let you focus on data, instead of file formats
================================================================================

:Author: C.W.
:Source code: http://github.com/pyexcel/pyexcel.git
:Issues: http://github.com/pyexcel/pyexcel/issues
:License: New BSD License
:Development: |release|
:Released: |version|
:Generated: |today|

Introduction
-------------

**pyexcel** provides **one** application programming interface to read,
manipulate and write data in different excel formats. This library makes
information processing involving excel files an enjoyable task. The data in
excel files can be turned into :ref:`array or dict<a-list-of-data-structures>`
with least code, vice versa. This library focuses on data
processing using excel files as storage media hence fonts, colors and charts
were not and will not be considered.

The idea originated from the common usability problem when developing an excel file
driven web applications for non-technical office workers: such as office assistant,
human resource administrator. The fact is that not all people know the
difference among various excel formats: csv, xls, xlsx. Instead of training those people
about file formats, this library helps web developers to handle most of the excel file
formats by providing a common programming interface. To add a specific excel file format
to you application, all you need is to install an extra pyexcel plugin. No code change
to your application. Looking at the community, this library and its associated ones try
to become a small and easy to install alternative to Pandas.


.. note::

   Since version `0.2.2`, no longer a plugin should be explicitly imported.
   They are imported if they are installed. Please use pip to manage the
   plugins.

Installation
-------------

You can install it via pip:

.. code-block:: bash

    $ pip install pyexcel


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/pyexcel/pyexcel.git
    $ cd pyexcel
    $ python setup.py install

For individual excel file formats, please install them as you wish:

.. _file-format-list:
.. _a-map-of-plugins-and-file-formats:

.. table:: A list of file formats supported by external plugins

   ================= ======================= ============= ==================
   Package name      Supported file formats  Dependencies  Python versions
   ================= ======================= ============= ==================
   `pyexcel-io`_     csv, csvz [#f1]_, tsv,                2.6, 2.7, 3.3,
                     tsvz [#f2]_                           3.4, 3.5, 3.6
                                                           pypy
   `pyexcel-xls`_    xls, xlsx(read only),   `xlrd`_,      same as above
                     xlsm(read only)         `xlwt`_
   `pyexcel-xlsx`_   xlsx                    `openpyxl`_   same as above
   `pyexcel-xlsxw`_  xlsx(write only)        `XlsxWriter`_ same as above
   `pyexcel-ods3`_   ods                     `ezodf`_,     2.6, 2.7, 3.3, 3.4
                                             lxml          3.5, 3.6
   `pyexcel-ods`_    ods                     `odfpy`_      same as above
   `pyexcel-odsr`_   ods(read only)          lxml          same as above
   `pyexcel-text`_   (write only)json, rst,  `tabulate`_   2.6, 2.7, 3.3, 3.4
                     mediawiki, html,                      3.5, pypy, pypy3
                     latex, grid, pipe,
                     orgtbl, plain simple
   ================= ======================= ============= ==================

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-odsr: https://github.com/pyexcel/pyexcel-odsr
.. _pyexcel-xlsxw: https://github.com/pyexcel/pyexcel-xlsxw

.. _xlrd: https://github.com/python-excel/xlrd
.. _xlwt: https://github.com/python-excel/xlwt
.. _openpyxl: https://bitbucket.org/openpyxl/openpyxl
.. _XlsxWriter: https://github.com/jmcnamara/XlsxWriter
.. _ezodf: https://github.com/T0ha/ezodf
.. _odfpy: https://github.com/eea/odfpy

.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text
.. _tabulate: https://bitbucket.org/astanin/python-tabulate

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file

For compatibility tables of pyexcel-io plugins, please click `here <http://pyexcel-io.readthedocs.io/en/latest/#id5>`_

.. table:: Plugin compatibility table

    ======= ========== ============ ============= ====================
    pyexcel pyexcel-io pyexcel-text pyexcel-chart pyexcel-handsontable
    ======= ========== ============ ============= ====================
    0.5.0+  0.3.0      0.2.6(cming) 0.0.1(coming) 0.0.1(coming)
    0.4.0+  0.3.0+     0.2.5
    0.3.0+  0.2.3      0.2.4
    0.2.2+  0.2.0+     0.2.1+
    0.2.1   0.1.0      0.2.0
    0.2.0   0.1.0      0.1.0+
    ======= ========== ============ ============= ====================


Usage
------

.. testcode::
   :hide:

   >>> import pyexcel
   >>> # make sure you had pyexcel-xls pip-installed
   >>> a_list_of_dictionaries = [
   ...     {
   ...         "Name": 'Adam',
   ...         "Age": 28
   ...     },
   ...     {
   ...         "Name": 'Beatrice',
   ...         "Age": 29
   ...     },
   ...     {
   ...         "Name": 'Ceri',
   ...         "Age": 30
   ...     },
   ...     {
   ...         "Name": 'Dean',
   ...         "Age": 26
   ...     }
   ... ]
   >>> pyexcel.save_as(records=a_list_of_dictionaries, dest_file_name="your_file.xls")

Suppose you want to process the following excel data :

========= ====
Name      Age
========= ====
Adam      28
Beatrice  29
Ceri      30
Dean      26
========= ====

Here are the example usages:

.. code-block:: python

   >>> import pyexcel as pe
   >>> records = pe.iget_records(file_name="your_file.xls")
   >>> for record in records:
   ...     print("%s is aged at %d" % (record['Name'], record['Age']))
   Adam is aged at 28
   Beatrice is aged at 29
   Ceri is aged at 30
   Dean is aged at 26

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file.xls")

Design
--------------------

.. toctree::

   design
   capability

Tutorial
----------
.. toctree::

   tutorial_file
   tutorial06
   tutorial_data_conversion
   attributes.rst
   bigdata
   tutorial
   tutorial05
   tutorial02
   tutorial03
   tutorial04
   logging
   migration_guide

Cook book
----------

.. toctree::

   cookbook
   sources

Real world cases
-------------------

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

Change log
-------------------

.. toctree::
   :maxdepth: 2

   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
