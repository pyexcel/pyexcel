`pyexcel` - Let you focus on data, instead of file formats
================================================================================

:Author: C.W.
:Source code: http://github.com/pyexcel/pyexcel.git
:Issues: http://github.com/pyexcel/pyexcel/issues
:License: New BSD License
:Released: |version|
:Generated: |today|

Introduction
-------------

**pyexcel** provides **one** application programming interface to read,
manipulate and write data in various excel formats. This library makes
information processing involving excel files an enjoyable task. The data in
excel files can be turned into :ref:`array or dict<a-list-of-data-structures>`
with minimal code and vice versa. This library focuses on data
processing using excel files as storage media hence fonts, colors and charts
were not and will not be considered.

The idea originated from the common usability problem: when an excel file
driven web application is delivered for non-developer users (ie: team assistant,
human resource administrator etc). The fact is that not everyone knows (or cares) about the
differences between various excel formats: csv, xls, xlsx are all the same to them. Instead of training those users
about file formats, this library helps web developers to handle most of the excel file
formats by providing a common programming interface. To add a specific excel file format type
to you application, all you need is to install an extra pyexcel plugin. Hence no code changes
to your application and no issues with excel file formats any more. Looking at the
community, this library and its associated ones try to become a small and easy to
install alternative to Pandas.


Support the project
================================================================================

If your company has embedded pyexcel and its components into a revenue generating
product, please support me on `github <https://github.com/sponsors/chfw>`_, `patreon <https://www.patreon.com/bePatron?u=5537627>`_
or `bounty source <https://salt.bountysource.com/teams/chfw-pyexcel>`_ to maintain
the project and develop it further.

If you are an individual, you are welcome to support me too and for however long
you feel like. As my backer, you will receive
`early access to pyexcel related contents <https://www.patreon.com/pyexcel/posts>`_.

And your issues will get prioritized if you would like to become my patreon as `pyexcel pro user`.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting posts.


Installation
-------------


You can install pyexcel via pip:

.. code-block:: bash

    $ pip install pyexcel


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/pyexcel.git
    $ cd pyexcel
    $ python setup.py install

For individual excel file formats, please install them as you wish:

.. _file-format-list:
.. _a-map-of-plugins-and-file-formats:

.. table:: A list of file formats supported by external plugins

   ======================== ======================= ================= ==================
   Package name              Supported file formats  Dependencies     Python versions
   ======================== ======================= ================= ==================
   `pyexcel-io`_            csv, csvz [#f1]_, tsv,                    2.6, 2.7, 3.3,
                            tsvz [#f2]_                               3.4, 3.5, 3.6
                                                                      pypy
   `pyexcel-xls`_           xls, xlsx(read only),   `xlrd`_,          same as above
                            xlsm(read only)         `xlwt`_
   `pyexcel-xlsx`_          xlsx                    `openpyxl`_       same as above
   `pyexcel-ods3`_          ods                     `pyexcel-ezodf`_, 2.6, 2.7, 3.3, 3.4
                                                    lxml              3.5, 3.6
   `pyexcel-ods`_           ods                     `odfpy`_          same as above
   ======================== ======================= ================= ==================

.. table:: Dedicated file reader and writers

   ======================== ======================= ================= ==================
   Package name              Supported file formats  Dependencies     Python versions
   ======================== ======================= ================= ==================
   `pyexcel-xlsxw`_         xlsx(write only)        `XlsxWriter`_     Python 2 and 3
   `pyexcel-xlsxr`_         xlsx(read only)         lxml              same as above
   `pyexcel-xlsbr`_         xlsx(read only)         pyxlsb            same as above
   `pyexcel-odsr`_          read only for ods, fods lxml              same as above
   `pyexcel-odsw`_          write only for ods      loxun             same as above
   `pyexcel-htmlr`_         html(read only)         lxml,html5lib     same as above
   `pyexcel-pdfr`_          pdf(read only)          pdftables         Python 2 only.
   ======================== ======================= ================= ==================


.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-odsr: https://github.com/pyexcel/pyexcel-odsr
.. _pyexcel-odsw: https://github.com/pyexcel/pyexcel-odsw
.. _pyexcel-pdfr: https://github.com/pyexcel/pyexcel-pdfr

.. _pyexcel-xlsxw: https://github.com/pyexcel/pyexcel-xlsxw
.. _pyexcel-xlsxr: https://github.com/pyexcel/pyexcel-xlsxr
.. _pyexcel-xlsbr: https://github.com/pyexcel/pyexcel-xlsbr
.. _pyexcel-htmlr: https://github.com/pyexcel/pyexcel-htmlr

.. _xlrd: https://github.com/python-excel/xlrd
.. _xlwt: https://github.com/python-excel/xlwt
.. _openpyxl: https://bitbucket.org/openpyxl/openpyxl
.. _XlsxWriter: https://github.com/jmcnamara/XlsxWriter
.. _pyexcel-ezodf: https://github.com/pyexcel/pyexcel-ezodf
.. _odfpy: https://github.com/eea/odfpy

.. table:: Other data renderers

   ======================== ======================= ================= ==================
   Package name              Supported file formats  Dependencies     Python versions
   ======================== ======================= ================= ==================
   `pyexcel-text`_          write only:rst,         `tabulate`_       2.6, 2.7, 3.3, 3.4
                            mediawiki, html,                          3.5, 3.6, pypy
                            latex, grid, pipe,
                            orgtbl, plain simple
                            read only: ndjson
                            r/w: json
   `pyexcel-handsontable`_  handsontable in html    `handsontable`_   same as above
   `pyexcel-pygal`_         svg chart               `pygal`_          2.7, 3.3, 3.4, 3.5
                                                                      3.6, pypy
   `pyexcel-sortable`_      sortable table in html  `csvtotable`_     same as above
   `pyexcel-gantt`_         gantt chart in html     `frappe-gantt`_   except pypy, same
                                                                      as above
   ======================== ======================= ================= ==================

.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text
.. _tabulate: https://bitbucket.org/astanin/python-tabulate
.. _pyexcel-handsontable: https://github.com/pyexcel/pyexcel-handsontable
.. _handsontable: https://cdnjs.com/libraries/handsontable
.. _pyexcel-pygal: https://github.com/pyexcel/pyexcel-chart
.. _pygal: https://github.com/Kozea/pygal
.. _pyexcel-matplotlib: https://github.com/pyexcel/pyexcel-matplotlib
.. _matplotlib: https://matplotlib.org
.. _pyexcel-sortable: https://github.com/pyexcel/pyexcel-sortable
.. _csvtotable: https://github.com/vividvilla/csvtotable
.. _pyexcel-gantt: https://github.com/pyexcel/pyexcel-gantt
.. _frappe-gantt: https://github.com/frappe/gantt

In order to manage the list of plugins installed, you need to use pip to add or remove
a plugin. When you use virtualenv, you can have different plugins per virtual
environment. In the situation where you have multiple plugins that does the same thing
in your environment, you need to tell pyexcel which plugin to use per function call.
For example, pyexcel-ods and pyexcel-odsr, and you want to get_array to use pyexcel-odsr.
You need to append get_array(..., library='pyexcel-odsr').

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file

For compatibility tables of pyexcel-io plugins, please click `here <http://pyexcel-io.readthedocs.io/en/latest/#id5>`_

.. table:: Plugin compatibility table

    ======== ========== ============= ==================== ============= =============
    pyexcel  pyexcel-io pyexcel-text  pyexcel-handsontable pyexcel-pygal pyexcel-gantt
    ======== ========== ============= ==================== ============= =============
    0.5.15+  0.5.19+    0.2.6+        0.0.1+               0.0.1         0.0.1
    0.5.14   0.5.18     0.2.6+        0.0.1+               0.0.1         0.0.1
    0.5.10+  0.5.11+    0.2.6+        0.0.1+               0.0.1         0.0.1
    0.5.9.1+ 0.5.9.1+   0.2.6+        0.0.1                0.0.1         0.0.1
    0.5.4+   0.5.1+     0.2.6+        0.0.1                0.0.1         0.0.1
    0.5.0+   0.4.0+     0.2.6+        0.0.1                0.0.1         0.0.1
    0.4.0+   0.3.0+     0.2.5
    ======== ========== ============= ==================== ============= =============


.. table:: a list of support file formats

    ============ =======================================================
    file format  definition
    ============ =======================================================
    csv          comma separated values
    tsv          tab separated values
    csvz         a zip file that contains one or many csv files
    tsvz         a zip file that contains one or many tsv files
    xls          a spreadsheet file format created by
                 MS-Excel 97-2003 [#f1]_
    xlsx         MS-Excel Extensions to the Office Open XML
                 SpreadsheetML File Format. [#f2]_
    xlsm         an MS-Excel Macro-Enabled Workbook file
    ods          open document spreadsheet
    fods         flat open document spreadsheet
    json         java script object notation
    html         html table of the data structure
    simple       simple presentation
    rst          rStructured Text presentation of the data
    mediawiki    media wiki table
    ============ =======================================================


.. [f1] quoted from `whatis.com <http://whatis.techtarget.com/fileformat/XLS-Worksheet-file-Microsoft-Excel>`_. Technical details can be found at `MSDN XLS <https://msdn.microsoft.com/en-us/library/office/gg615597(v=office.14).aspx>`_
.. [f2] xlsx is used by MS-Excel 2007, more information can be found at `MSDN XLSX <https://msdn.microsoft.com/en-us/library/dd922181(v=office.12).aspx>`_


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

.. pyexcel-table::

   ---pyexcel:example table---
   Name,Age
   Adam,28
   Beatrice,29
   Ceri,30
   Dean,26


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
   >>> pe.free_resources()

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file.xls")

Design
--------------------

.. toctree::

   design
   capability
   architecture

New tutorial
----------
.. toctree::

   quickstart
   two-liners
   iodrivers
   webdev
   renderers
   sheet
   book
   database

Old tutorial
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

Cook book
----------

.. toctree::

   cookbook
   sources

Real world cases
-------------------

.. toctree::

   answers
   showcases/db_injection

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
   logging
   pyinstaller
   plugin_howto

Change log
-------------------

.. toctree::
   :maxdepth: 2

   migration_guide
   changelog
   note_on_pypy


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
