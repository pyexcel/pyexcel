Change log
================================================================================

0.3.0 - Unreleased
--------------------------------------------------------------------------------

Added:
********************************************************************************

#. file type setters for Sheet and Book, and its documentation
#. `iget_records` returns a generator for a list of records and should have
   better memory performance, especially dealing with large csv files.

Removed:
********************************************************************************

#. `content` and `out_file` as function parameters to the signature functions are
   no longer supported. 
#. SourceFactory and RendererFactory are removed

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
