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
with least code, vice versa. And ready-made custom :ref:`filters<filters>`
and :ref:`formatters<formatters>` can be applied. This library focuses on data
processing using excel files as storage media hence fonts, colors and charts
were not and will not be considered.

Excel files are de-facto file format for information sharing in non-software
centric organisations. Excel files are not only used for mathematical
computation in financial institutions but also used for many other purposes
in an office work environment. This is largely caused by wide adoption of
Microsoft Office. Comparing the existing, mathematics savvy Pandas library,
this library intends to help data processing job where data extraction is more
important than data analysis. In such context, ease of use, and low overhead is
preferred, while Pandas is as big as 4MB and contains hundreds of potentially
useful functions.

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
                     tsvz [#f2]_                           3.4, 3.5,
                                                           pypy, pypy3
   `pyexcel-xls`_    xls, xlsx(read only),   xlrd, xlwt    same as above
                     xlsm(read only)                       
                                                           
   `pyexcel-xlsx`_   xlsx                    openpyxl      same as above
   `pyexcel-xlsxw`_  xlsx(write only)        xlsxwriter    same as above
   `pyexcel-ods3`_   ods                     ezodf, lxml   2.6, 2.7, 3.3, 3.4
                                                           3.5
   `pyexcel-ods`_    ods                     odfpy         same as above
   `pyexcel-text`_   (write only)json, rst,  tabulate      2.6, 2.7, 3.3, 3.4
                     mediawiki, html,                      3.5, pypy, pypy3
                     latex, grid, pipe,
                     orgtbl, plain simple
   ================= ======================= ============= ==================

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-xlsxw: https://github.com/pyexcel/pyexcel-xlsxw

.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file

For compatibility tables of pyexcel-io plugins, please click `here <http://pyexcel-io.readthedocs.io/en/latest/#id5>`_

.. table:: Plugin compatibility table

    ======= ========== ============
    pyexcel pyexcel-io pyexcel-text
    ======= ========== ============
    0.3.0   0.2.0+     0.2.1+
    0.2.2+  0.2.0+     0.2.1+
    0.2.1   0.1.0      0.2.0
    0.2.0   0.1.0      0.1.0+
    ======= ========== ============


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
   tutorial
   tutorial05
   tutorial02
   tutorial03
   tutorial04
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
