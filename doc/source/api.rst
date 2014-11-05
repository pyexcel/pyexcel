=============
API Reference
=============

.. currentmodule:: pyexcel
.. _api:

This is intended for users of pyexcel

   
Sheet
=====

Constructor
-----------

.. autosummary::
   :toctree: generated/

   load
   load_from_memory
   Sheet

Attributes
-----------

.. autosummary::
   :toctree: generated/

   Sheet.row
   Sheet.column
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
   Sheet.is_series


Data series
------------

Any row as column names
************************

.. autosummary::
   :toctree: generated/

   Sheet.index_by_column
   Sheet.rownames
   Sheet.named_row_at
   Sheet.set_named_row_at
   Sheet.delete_named_row_at


Any column as row name
************************

.. autosummary::
   :toctree: generated/

   Sheet.index_by_row
   Sheet.colnames
   Sheet.named_column_at
   Sheet.set_named_column_at
   Sheet.delete_named_column_at

Formatting
------------------

.. autosummary::
   :toctree: generated/

   Sheet.format
   Sheet.apply_formatter
   Sheet.add_formatter
   Sheet.remove_formatter
   Sheet.clear_formatters
   Sheet.freeze_formatters

Filtering
-----------

.. autosummary::
   :toctree: generated/

   Sheet.filter
   Sheet.add_filter
   Sheet.remove_filter
   Sheet.clear_formatters
   Sheet.freeze_filters

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
		

Save changes
--------------

.. autosummary::
   :toctree: generated/

   Sheet.save_as
   Sheet.save_to_memory


Book 
=====

Constructor
------------

.. autosummary::
   :toctree: generated

   load_book
   load_book_from_memory
   Book

Attribute
------------

.. autosummary::
   :toctree: generated

   Book.number_of_sheets
   Book.sheet_names

Conversions
-------------

.. autosummary::
   :toctree: generated

   Book.to_dict

Save changes
-------------

.. autosummary::
   :toctree: generated

   Book.save_as
   Book.save_to_memory
