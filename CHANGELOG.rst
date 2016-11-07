Change log
================================================================================

0.3.3 - unreleased
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `# 63 <https://github.com/pyexcel/pyexcel/issues/63>`_: cannot display
   empty sheet(hence book with empty sheet) as texttable


0.3.2 - 2.11.2016
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
