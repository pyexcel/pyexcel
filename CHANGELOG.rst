Change log
================================================================================

0.5.0 - unreleased
--------------------------------------------------------------------------------

Added
********************************************************************************

#. Sheet.top() and Sheet.top_left() for data browsing
#. add html as default rich display in Jupyter notebook. It is dependent on
   pyexcel-text.
#. new dictionary source supported: a dictionary of key value pair could be
   read into a sheet.
#. added dynamic external plugin loading. meaning if a pyexcel plugin
   is installed, and has `__pyexcel_plugins__` signature in its
   __init__.py, it will be loaded implicitly. And this change would remove
   un-necessary info log for those who do not use pyexcel-text and pyexcel-chart
#. save_book_as before 0.5.0 becomes isave_book_as and save_book_as in 0.5.0
   convert BookStream to Book before saving.

Removed
********************************************************************************

#. pyexcel.Writer and pyexcel.BookWriter were removed
#. pyexcel.load_book_from_sql and pyexcel.load_from_sql were removed
#. pyexcel.deprecated.load_from_query_sets,
   pyexcel.deprecated.load_book_from_django_models and
   pyexcel.deprecated.load_from_django_model were removed


0.4.4 - 06.02.2017
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `#68 <https://github.com/pyexcel/pyexcel/issues/68>`_: regression
   save_to_memory() should have returned a stream instance which has
   been reset to zero if possible. The exception is sys.stdout, which cannot
   be reset.

#. `#74 <https://github.com/pyexcel/pyexcel/issues/74>`_: Not able to
   handle decimal.Decimal

Removed
********************************************************************************

#. remove get_{{file_type}}_stream functions from pyexcel.Sheet and
   pyexel.Book introduced since 0.4.3.


0.4.3 - 26.01.2017
--------------------------------------------------------------------------------

Added
********************************************************************************

#. '.stream' attribte are attached to `~pyexcel.Sheet` and
   `~pyexcel.Book` to get direct access the underneath stream
   in responding to file type attributes, suchs sheet.xls. it helps provide a custom
   stream to external world, for example, Sheet.stream.csv gives a text stream
   that contains csv formatted data. Book.stream.xls returns a xls format
   data in a byte stream.

Updated
********************************************************************************

#. Better error reporting when an unknown parameters or unsupported file types
   were given to the signature functions.


0.4.2 - 17.01.2017
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. Raise exception if the incoming sheet does not have column names. In other
   words, only sheet with column names could be saved to database. sheet with
   row names cannot be saved. The alternative is to tranpose the sheet, then
   name_columns_by_row and then save.
#. fix iget_records where a non-uniform content should be given,
   e.g. [["x", "y"], [1, 2], [3]], some record would become non-uniform, e.g.
   key 'y' would be missing from the second record.
#. `skip_empty_rows` is applicable when saving a python data structure to
   another data source. For example, if your array contains a row which is
   consisted of empty string, such as ['', '', '' ... ''], please specify
   `skip_empty_rows=False` in order to preserve it. This becomes subtle when
   you try save a python dictionary where empty rows is not easy to be spotted.
#. `#69  <https://github.com/pyexcel/pyexcel/issues/69>`_: better documentation
   for save_book_as.

0.4.1 - 23.12.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `#68  <https://github.com/pyexcel/pyexcel/issues/68>`_: regression
   save_to_memory() should have returned a stream instance.


0.4.0 - 22.12.2016
--------------------------------------------------------------------------------

Added
********************************************************************************

#. `Flask-Excel issue 19 <https://github.com/pyexcel/Flask-Excel/issues/19>`_
   allow sheet_name parameter
#. `pyexcel-xls issue 11 <https://github.com/pyexcel/pyexcel-xls/issues/11>`_
   case-incenstive for file_type. `xls` and `XLS` are treated in the same way


Updated
********************************************************************************

#. `# 66 <https://github.com/pyexcel/pyexcel/issues/66>`_: `export_columns` is
   ignored
#. Update dependency on pyexcel-io v0.3.0


0.3.3 - 07.11.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `# 63 <https://github.com/pyexcel/pyexcel/issues/63>`_: cannot display
   empty sheet(hence book with empty sheet) as texttable


0.3.2 - 02.11.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `# 62 <https://github.com/pyexcel/pyexcel/issues/62>`_: optional module
   import error become visible.


0.3.0 - 28.10.2016
--------------------------------------------------------------------------------

.. _version_o_three:

Added:
********************************************************************************

#. file type setters for Sheet and Book, and its documentation
#. `iget_records` returns a generator for a list of records and should have
   better memory performance, especially dealing with large csv files.
#. `iget_array` returns a generator for a list of two dimensional array and
   should have better memory performance, especially dealing with large csv
   files.
#. Enable pagination support, and custom row renderer via pyexcel-io v0.2.3

Updated
********************************************************************************

#. Take `isave_as` out from `save_as`. Hence two functions are there for save
   a sheet as
#. `# 60 <https://github.com/pyexcel/pyexcel/issues/60>`_: encode 'utf-8' if
   the console is of ascii encoding.
#. `# 59 <https://github.com/pyexcel/pyexcel/issues/59>`_: custom row
   renderer
#. `# 56 <https://github.com/pyexcel/pyexcel/issues/56>`_: set cell value does
   not work
#. pyexcel.transpose becomes `pyexcel.sheets.transpose`
#. iterator functions of `pyexcel.Sheet` were converted to generator
   functions

   * `pyexcel.Sheet.enumerate()`
   * `pyexcel.Sheet.reverse()`
   * `pyexcel.Sheet.vertical()`
   * `pyexcel.Sheet.rvertical()`
   * `pyexcel.Sheet.rows()`
   * `pyexcel.Sheet.rrows()`
   * `pyexcel.Sheet.columns()`
   * `pyexcel.Sheet.rcolumns()`
   * `pyexcel.Sheet.named_rows()`
   * `pyexcel.Sheet.named_columns()`

#. `~pyexcel.Sheet.save_to_memory` and `~pyexcel.Book.save_to_memory`
   return the actual content. No longer they will return a io object hence
   you cannot call getvalue() on them.

Removed:
********************************************************************************

#. `content` and `out_file` as function parameters to the signature functions are
   no longer supported.
#. SourceFactory and RendererFactory are removed
#. The following methods are removed

   * `pyexcel.to_array`
   * `pyexcel.to_dict`
   * `pyexcel.utils.to_one_dimensional_array`
   * `pyexcel.dict_to_array`
   * `pyexcel.from_records`
   * `pyexcel.to_records`

#. `pyexcel.Sheet.filter` has been re-implemented and all filters were
   removed:

   * `pyexcel.filters.ColumnIndexFilter`
   * `pyexcel.filters.ColumnFilter`
   * `pyexcel.filters.RowFilter`
   * `pyexcel.filters.EvenColumnFilter`
   * `pyexcel.filters.OddColumnFilter`
   * `pyexcel.filters.EvenRowFilter`
   * `pyexcel.filters.OddRowFilter`
   * `pyexcel.filters.RowIndexFilter`
   * `pyexcel.filters.SingleColumnFilter`
   * `pyexcel.filters.RowValueFilter`
   * `pyexcel.filters.NamedRowValueFilter`
   * `pyexcel.filters.ColumnValueFilter`
   * `pyexcel.filters.NamedColumnValueFilter`
   * `pyexcel.filters.SingleRowFilter`

#. the following functions have been removed

   * `add_formatter`
   * `remove_formatter`
   * `clear_formatters`
   * `freeze_formatters`
   * `add_filter`
   * `remove_filter`
   * `clear_filters`
   * `freeze_formatters`

#. `pyexcel.Sheet.filter` has been re-implemented and all filters were
   removed:

   * pyexcel.formatters.SheetFormatter


0.2.5 - 31.08.2016
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. `# 58 <https://github.com/pyexcel/pyexcel/issues/58>`_: texttable should
   have been made as compulsory requirement


0.2.4 - 14.07.2016
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. For python 2, writing to sys.stdout by pyexcel-cli raise IOError.

0.2.3 - 11.07.2016
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. For python 3, do not seek 0 when saving to memory if sys.stdout is passed on.
   Hence, adding support for sys.stdin and sys.stdout.

0.2.2 - 01.06.2016
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. Explicit imports, no longer needed
#. Depends on latest setuptools 18.0.1
#. NotImplementedError will be raised if parameters to core functions are not supported, e.g. get_sheet(cannot_find_me_option="will be thrown out as NotImplementedError")

0.2.1 - 23.04.2016
--------------------------------------------------------------------------------

Added:
********************************************************************************

#. add pyexcel-text file types as attributes of pyexcel.Sheet and pyexcel.Book, related to `issue 31 <https://github.com/pyexcel/pyexcel/issues/31>`__
#. auto import pyexcel-text if it is pip installed

Updated:
********************************************************************************

#. code refactoring done for easy addition of sources.
#. bug fix `issue 29 <https://github.com/pyexcel/pyexcel/issues/29>`__, Even if the format is a string it is displayed as a float
#. pyexcel-text is no longer a plugin to pyexcel-io but to pyexcel.sources, see `pyexcel-text issue #22 <https://github.com/pyexcel/pyexcel-text/issues/22>`__

Removed:
********************************************************************************
#. pyexcel.presentation is removed. No longer the internal decorate @outsource is used. related to `issue 31 <https://github.com/pyexcel/pyexcel/issues/31>`_


0.2.0 - 17.01.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. adopt pyexcel-io yield key word to return generator as content
#. pyexcel.save_as and pyexcel.save_book_as get performance improvements
