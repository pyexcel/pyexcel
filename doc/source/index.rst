.. pyexcel documentation master file, created by
   sphinx-quickstart on Tue Sep  9 08:53:12 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`pyexcel` - Let you focus on data, instead of file formats
================================================================================

:Author: C.W.
:Source code: http://github.com/pyexcel/pyexcel
:Issues: http://github.com/pyexcel/pyexcel/issues
:License: New BSD License
:Version: |version|
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
in an office work environment. This is largely casued by wide adoption of
Microsoft Office. Comparing the existing, mathematics savvy Pandas library,
this library intends to help data processing job where data extraction is more
important than data analysis. In such context, ease of use, and low overhead is
preferred, while Pandas is as big as 4MB and contains hundreds of potentially
useful functions.


Getting the source
--------------------------------------------------------------------------------


Source code is hosted in github. You can get it using git client:

.. code-block:: bash

    $ git clone http://github.com/pyexcel/pyexcel.git

Installation
-------------

You can install it via pip:

.. code-block:: bash

    $ pip install pyexcel

For individual excel file formats, please install them as you wish:

.. _a-map-of-plugins-and-file-formats:
.. table:: a map of plugins and supported excel file formats

   ========= ======================= ============= ======================== =============================	
   Plugin    Supported file formats  Dependencies  Python versions			 Comments
   ========= ======================= ============= ======================== =============================	
   pyexcel   csv, csvz [#f1]_, tsv,  `pyexcel-io`_ 2.6, 2.7, 3.3, 3.4, pypy 						
             tsvz [#f2]_     
   `xls`_    xls, xlsx(read only),   xlrd, xlwt    2.6, 2.7, 3.3, 3.4, pypy supports reading xlsx as well
             xlsm(read only)
   `xlsx`_   xlsx                    openpyxl      2.6, 2.7, 3.3, 3.4, pypy 					
   `ods3`_   ods                     ezodf, lxml   2.6, 2.7, 3.3, 3.4							
   `ods`_    ods (python 2.6, 2.7)   odfpy         2.6, 2.7									
   `text`_   json, rst, mediawiki,   tabulate      2.6, 2.7, 3.3, 3.4, pypy writing to files only
             latex, grid, etc.
   ========= ======================= ============= ======================== =============================

.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _xls: https://github.com/pyexcel/pyexcel-xls
.. _xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _ods: https://github.com/pyexcel/pyexcel-ods
.. _ods3: https://github.com/pyexcel/pyexcel-ods3
.. _text: https://github.com/pyexcel/pyexcel-text


Please import them before you start to access the desired file formats::

    from pyexcel.ext import plugin

or::

    import pyexcel.ext.plugin

.. table:: Plugin compatibility table

    ======= ========== =========== ============ ============ ============ ============
    pyexcel pyexcel-io xls         xlsx         ods          ods3         text  
    ======= ========== =========== ============ ============ ============ ============
    0.2.0   0.1.0  
    ======= ========== =========== ============ ============ ============ ============

Usage
------

.. testcode::
   :hide:

   >>> import pyexcel
   >>> import pyexcel.ext.xls
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
   >>> import pyexcel.ext.xls # import it to handle xls file
   >>> import pyexcel.ext.xlsx # import it to handle xlsx file
   >>> records = pe.get_records(file_name="your_file.xls")
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

   tutorial
   tutorial05
   tutorial02
   tutorial_data_conversion
   tutorial03
   tutorial04
   tutorial_file
   tutorial06
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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file
