
=============
API Reference
=============

.. currentmodule:: pyexcel
.. _api:


This is intended for users of pyexcel.

.. _signature-functions:

Signature functions
====================

These flags can be passed on to control plugin behaviors:

auto_detect_int
--------------------------------------------------------------------------------

Automatically convert float values to integers if the float number has no
decimal values(e.g. 1.00). By default, it does the detection. Setting it to
False will turn on this behavior

It has no effect on pyexcel-xlsx because it does that by default.


auto_detect_float
----------------------

Automatically convert text to float values if possible. This applies only
pyexcel-io where csv, tsv, csvz and tsvz formats are supported.  By default,
it does the detection. Setting it to False will turn on this behavior


auto_detect_datetime
-----------------------

Automatically convert text to python datetime if possible. This applies only
pyexcel-io where csv, tsv, csvz and tsvz formats are supported.  By default,
it does the detection. Setting it to False will turn on this behavior


library
-------------------------

Name a pyexcel plugin to handle a file format. In the situation where multiple
plugins were pip installed, it is confusing for pyexcel on which plugin to
handle the file format. For example, both pyexcel-xlsx and pyexcel-xls reads
xlsx format. Now since version 0.2.2, you can pass on `library="pyexcel-xls"`
to handle xlsx in a specific function call.

It is better to uninstall the unwanted pyexcel plugin using pip if two plugins
for the same file type are not absolutely necessary.

.. _conversion-from:


Obtaining data from excel file
-------------------------------

.. autosummary::
   :toctree: generated/

   get_array
   get_dict
   get_records
   iget_records
   get_book_dict
   get_book
   get_sheet

.. _conversion-to:

Saving data to excel file
--------------------------

.. autosummary::
   :toctree: generated/

   save_as
   save_book_as
   
Cookbook
==========

.. autosummary::
   :toctree: generated/

   merge_csv_to_a_book
   merge_all_to_a_book
   split_a_book
   extract_a_sheet_from_a_book

   
Book 
=====

Here's the entity relationship between Book, Sheet, Row and Column

.. image:: entity-relationship-diagram.png

Constructor
------------

.. autosummary::
   :toctree: generated/

   Book

Attribute
------------

.. autosummary::
   :toctree: generated/

   Book.bookdict
   Book.url
   Book.csv
   Book.tsv
   Book.csvz
   Book.tsvz
   Book.xls
   Book.xlsx
   Book.ods
   Book.plain
   Book.simple
   Book.grid
   Book.pipe
   Book.orgtbl
   Book.rst
   Book.mediawiki
   Book.latex
   Book.latex_booktabs
   Book.json
   Book.html
   Book.number_of_sheets
   Book.sheet_names

Conversions
-------------

.. autosummary::
   :toctree: generated/

   Book.to_dict

Save changes
-------------

.. autosummary::
   :toctree: generated/

   Book.save_as
   Book.save_to_memory
   Book.save_to_database

Sheet
=====


Constructor
-----------

.. autosummary::
   :toctree: generated/

   Sheet

Save changes
--------------

.. autosummary::
   :toctree: generated/

   Sheet.save_as
   Sheet.save_to_memory
   Sheet.save_to_database

Attributes
-----------

.. autosummary::
   :toctree: generated/

   Sheet.array
   Sheet.records
   Sheet.dict
   Sheet.content
   Sheet.url
   Sheet.csv
   Sheet.tsv
   Sheet.csvz
   Sheet.tsvz
   Sheet.xls
   Sheet.xlsx
   Sheet.ods
   Sheet.plain
   Sheet.simple
   Sheet.grid
   Sheet.pipe
   Sheet.orgtbl
   Sheet.rst
   Sheet.mediawiki
   Sheet.latex
   Sheet.latex_booktabs
   Sheet.json
   Sheet.html
   Sheet.number_of_rows
   Sheet.number_of_columns
   Sheet.row_range
   Sheet.column_range

Iteration
-----------------

.. autosummary::
   :toctree: generated/

   Sheet.rows
   Sheet.rrows
   Sheet.columns
   Sheet.rcolumns
   Sheet.enumerate
   Sheet.reverse
   Sheet.vertical
   Sheet.rvertical


Cell access
------------------

.. autosummary::
   :toctree: generated/

   Sheet.cell_value
   Sheet.__getitem__

Row access
------------------

.. autosummary::
   :toctree: generated/

   Sheet.row_at
   Sheet.set_row_at
   Sheet.delete_rows
   Sheet.extend_rows

Column access
--------------

.. autosummary::
   :toctree: generated/

   Sheet.column_at
   Sheet.set_column_at
   Sheet.delete_columns
   Sheet.extend_columns


Data series
------------


Any column as row name
************************

.. autosummary::
   :toctree: generated/

   Sheet.name_columns_by_row
   Sheet.rownames
   Sheet.named_column_at
   Sheet.set_named_column_at
   Sheet.delete_named_column_at


Any row as column name
************************

.. autosummary::
   :toctree: generated/

   Sheet.name_rows_by_column
   Sheet.colnames
   Sheet.named_row_at
   Sheet.set_named_row_at
   Sheet.delete_named_row_at

   
Formatting
------------------

.. autosummary::
   :toctree: generated/

   Sheet.format
   Sheet.apply_formatter

Filtering
-----------

.. autosummary::
   :toctree: generated/

   Sheet.filter

Conversion
-------------

.. autosummary::
   :toctree: generated/

   Sheet.to_array
   Sheet.to_dict
   Sheet.to_records

Anti-conversion
----------------

.. autosummary::
   :toctree: generated/

   dict_to_array
   from_records

Transformation
----------------

.. autosummary::
   :toctree: generated/

   Sheet.transpose
   Sheet.map
   Sheet.region
   Sheet.cut
   Sheet.paste
        

.. _formatters:

Data formatters
================

.. currentmodule:: pyexcel.sheets.formatters

.. autosummary::
   :toctree: generated/

   ColumnFormatter
   NamedColumnFormatter
   RowFormatter
   NamedRowFormatter
   SheetFormatter
   
.. _filters:

Data Filters
===============

.. currentmodule:: pyexcel.sheets.filters

.. autosummary::
   :toctree: generated/

   ColumnFilter
   SingleColumnFilter
   OddColumnFilter
   EvenColumnFilter
   ColumnValueFilter
   RowFilter
   SingleRowFilter
   OddRowFilter
   EvenRowFilter
   RowValueFilter
   RegionFilter
