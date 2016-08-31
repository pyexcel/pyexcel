========================================================
{{name}} - Let you focus on data, instead of file formats
========================================================

.. image:: https://api.travis-ci.org/{{name}}/{{name}}.svg?branch=master
    :target: http://travis-ci.org/{{name}}/{{name}}

.. image:: https://codecov.io/github/{{name}}/{{name}}/coverage.svg?branch=master
    :target: https://codecov.io/github/{{name}}/{{name}}?branch=master

.. image:: https://readthedocs.org/projects/{{name}}/badge/?verssion=latest
    :target: http://{{name}}.readthedocs.org/en/latest/


{%include "constraints.rst.jj2" %}


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

{% include "plugins-list.rst.jj2"%}

Installation
============

{%include "installation.rst.jj2" %}

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

{%include "developer_guide.rst.jj2" %}

{%include "license.rst.jj2" %}


Acknowledgement
===============

All great work have done by odf, ezodf(2), xlrd, xlwt, tabulate and other individual developers. This library unites only the data access code.

