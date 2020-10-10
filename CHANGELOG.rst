Change log
================================================================================

0.6.5 - 8.10.2020
--------------------------------------------------------------------------------

**Updated**

#. update queryset source to work with pyexcel-io 0.6.0

0.6.4 - 18.08.2020
--------------------------------------------------------------------------------

**Updated**

#. `#219 <https://github.com/pyexcel/pyexcel/issues/219>`_: book created from
   dict no longer discards order.

0.6.3 - 01.08.2020
--------------------------------------------------------------------------------

**fixed**

#. `#214 <https://github.com/pyexcel/pyexcel/issues/214>`_: remove leading and
   trailing whitespace for column names

**removed**

#. python 2 compatibility have been permanently removed.

0.6.2 - 8.06.2020
--------------------------------------------------------------------------------

**fixed**

#. `#109 <https://github.com/pyexcel/pyexcel/issues/109>`_: Control the column
   order when write the data output

0.6.1 - 02.05.2020
--------------------------------------------------------------------------------

**fixed**

#. `#203 <https://github.com/pyexcel/pyexcel/issues/203>`_: texttable was
   dropped out in 0.6.0 as compulsary dependency. end user may experience it
   when a sheet/table is printed in a shell. otherwise, new user of pyexcel
   won't see it. As of release date, no issues were created

0.6.0 - 21.04.2020
--------------------------------------------------------------------------------

**updated**

#. `#199 <https://github.com/pyexcel/pyexcel/issues/199>`_: += in place; = +
   shall return new instance
#. `#195 <https://github.com/pyexcel/pyexcel/issues/195>`_: documentation
   update. however small is welcome

**removed**

#. Dropping the test support for python version lower than 3.6. v0.6.0 should
   work with python 2.7 but is not guaranteed to work. Please upgrade to python
   3.6+.

0.5.15 - 07.07.2019
--------------------------------------------------------------------------------

**updated**

#. `#185 <https://github.com/pyexcel/pyexcel/issues/185>`_: fix a bug with http
   data source. The real fix lies in pyexcel-io v0.5.19. this release just put
   the version requirement in.

0.5.14 - 12.06.2019
--------------------------------------------------------------------------------

**updated**

#. `#182 <https://github.com/pyexcel/pyexcel/issues/182>`_: support
   dest_force_file_type on save_as and save_book_as

0.5.13 - 12.03.2019
--------------------------------------------------------------------------------

**updated**

#. `#176 <https://github.com/pyexcel/pyexcel/issues/176>`_: get_sheet
   {IndexError}list index out of range // XLSX can't be opened

0.5.12 - 25.02.2019
--------------------------------------------------------------------------------

**updated**

#. `#174 <https://github.com/pyexcel/pyexcel/issues/174>`_: include examples in
   tarbar

0.5.11 - 22.02.2019
--------------------------------------------------------------------------------

**updated**

#. `#169 <https://github.com/pyexcel/pyexcel/issues/169>`_: remove
   pyexcel-handsontalbe in test
#. add tests, and docs folder in distribution

0.5.10 - 3.12.2018
--------------------------------------------------------------------------------

**updated**

#. `#157 <https://github.com/pyexcel/pyexcel/issues/157>`_: Please use
   scan_plugins_regex, which lml 0.7 complains about
#. updated dependency on pyexcel-io to 0.5.11

0.5.9.1 - 30.08.2018
--------------------------------------------------------------------------------

**updated**

#. to require pyexcel-io 0.5.9.1 and use lml at least version 0.0.2

0.5.9 - 30.08.2018
--------------------------------------------------------------------------------

**added**

#. support __len__. len(book) returns the number of sheets and len(sheet)
   returns the number of rows
#. `#144 <https://github.com/pyexcel/pyexcel/issues/144>`_: memory-efficient way
   to read sheet names.
#. `#148 <https://github.com/pyexcel/pyexcel/issues/148>`_: force_file_type is
   introduced. When reading a file on a disk, this parameter allows you to
   choose a reader. i.e. csv reader for a text file. xlsx reader for a xlsx file
   but with .blob file suffix.
#. finally, pyexcel got import pyexcel.__version__

**updated**

#. Sheet.to_records() returns a generator now, saving memory
#. `#115 <https://github.com/pyexcel/pyexcel/issues/115>`_, Fix set membership
   test to run faster in python2
#. `#140 <https://github.com/pyexcel/pyexcel/issues/140>`_, Direct writes to
   cells yield weird results

0.5.8 - unreleased
--------------------------------------------------------------------------------

**added**

#. `#125 <https://github.com/pyexcel/pyexcel/issues/125>`_, sort book sheets

**updated**

#. `#126 <https://github.com/pyexcel/pyexcel/issues/126>`_, dest_sheet_name in
   save_as will set the sheet name in the output
#. `#115 <https://github.com/pyexcel/pyexcel/issues/115>`_, Fix set membership
   test to run faster in python2

0.5.7 - 11.01.2018
--------------------------------------------------------------------------------

**added**

#. `pyexcel-io#46 <https://github.com/pyexcel/pyexcel-io/issues/46>`_, expose
   `bulk_save` to developer.

0.5.6 - 23.10.2017
--------------------------------------------------------------------------------

**removed**

#. `#105 <https://github.com/pyexcel/pyexcel/issues/105>`_, remove gease from
   setup_requires, introduced by 0.5.5.
#. removed testing against python 2.6
#. `#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include LICENSE file
   in MANIFEST.in, meaning LICENSE file will appear in the released tar ball.

0.5.5 - 20.10.2017
--------------------------------------------------------------------------------

**removed**

#. `#105 <https://github.com/pyexcel/pyexcel/issues/105>`_, remove gease from
   setup_requires, introduced by 0.5.5.
#. removed testing against python 2.6
#. `#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include LICENSE file
   in MANIFEST.in, meaning LICENSE file will appear in the released tar ball.

0.5.4 - 27.09.2017
--------------------------------------------------------------------------------

**fixed**

#. `#100 <https://github.com/pyexcel/pyexcel/issues/100>`_, Sheet.to_dict() gets
   out of range error because there is only one row.

**updated**

#. Updated the baseline of pyexcel-io to 0.5.1.

0.5.3 - 01-08-2017
--------------------------------------------------------------------------------

**added**

#. `#95 <https://github.com/pyexcel/pyexcel/issues/95>`_, respect the order of
   records in iget_records, isave_as and save_as.
#. `#97 <https://github.com/pyexcel/pyexcel/issues/97>`_, new feature to allow
   intuitive initialization of pyexcel.Book.

0.5.2 - 26-07-2017
--------------------------------------------------------------------------------

**Updated**

#. embeded the enabler for pyexcel-htmlr. http source does not support text/html
   as mime type.

0.5.1 - 12.06.2017
--------------------------------------------------------------------------------

**Updated**

#. support saving SheetStream and BookStream to database targets. This is needed
   for pyexcel-webio and its downstream projects.

0.5.0 - 19.06.2017
--------------------------------------------------------------------------------

**Added**

#. Sheet.top() and Sheet.top_left() for data browsing
#. add html as default rich display in Jupyter notebook when pyexcel-text and
   pyexcel-chart is installed
#. add svg as default rich display in Jupyter notebook when pyexcel-chart and
   one of its implementation plugin(pyexcel-pygal, etc.) are is installed
#. new dictionary source supported: a dictionary of key value pair could be read
   into a sheet.
#. added dynamic external plugin loading. meaning if a pyexcel plugin is
   installed, it will be loaded implicitly. And this change would remove
   unnecessary info log for those who do not use pyexcel-text and pyexcel-gal
#. save_book_as before 0.5.0 becomes isave_book_as and save_book_as in 0.5.0
   convert BookStream to Book before saving.
#. `#83 <https://github.com/pyexcel/pyexcel/issues/83>`_, file closing mechanism
   is enfored. free_resource is added and it should be called when iget_array,
   iget_records, isave_as and/or isave_book_as are used.

**Updated**

#. array is passed to pyexcel.Sheet as reference. it means your array data will
   be modified.

**Removed**

#. pyexcel.Writer and pyexcel.BookWriter were removed
#. pyexcel.load_book_from_sql and pyexcel.load_from_sql were removed
#. pyexcel.deprecated.load_from_query_sets,
   pyexcel.deprecated.load_book_from_django_models and
   pyexcel.deprecated.load_from_django_model were removed
#. Removed plugin loading code and lml is used instead

0.4.5 - 17.03.2017
--------------------------------------------------------------------------------

**Updated**

#. `#80 <https://github.com/pyexcel/pyexcel/issues/80>`_: remove pyexcel-chart
   import from v0.4.x

0.4.4 - 06.02.2017
--------------------------------------------------------------------------------

**Updated**

#. `#68 <https://github.com/pyexcel/pyexcel/issues/68>`_: regression
   save_to_memory() should have returned a stream instance which has been reset
   to zero if possible. The exception is sys.stdout, which cannot be reset.
#. `#74 <https://github.com/pyexcel/pyexcel/issues/74>`_: Not able to handle
   decimal.Decimal

**Removed**

#. remove get_{{file_type}}_stream functions from pyexcel.Sheet and pyexcel.Book
   introduced since 0.4.3.

0.4.3 - 26.01.2017
--------------------------------------------------------------------------------

**Added**

#. '.stream' attribute are attached to `~pyexcel.Sheet` and `~pyexcel.Book` to
   get direct access the underneath stream in responding to file type
   attributes, such as sheet.xls. it helps provide a custom stream to external
   world, for example, Sheet.stream.csv gives a text stream that contains csv
   formatted data. Book.stream.xls returns a xls format data in a byte stream.

**Updated**

#. Better error reporting when an unknown parameters or unsupported file types
   were given to the signature functions.

0.4.2 - 17.01.2017
--------------------------------------------------------------------------------

**Updated**

#. Raise exception if the incoming sheet does not have column names. In other
   words, only sheet with column names could be saved to database. sheet with
   row names cannot be saved. The alternative is to transpose the sheet, then
   name_columns_by_row and then save.
#. fix iget_records where a non-uniform content should be given, e.g. [["x",
   "y"], [1, 2], [3]], some record would become non-uniform, e.g. key 'y' would
   be missing from the second record.
#. `skip_empty_rows` is applicable when saving a python data structure to
   another data source. For example, if your array contains a row which is
   consisted of empty string, such as ['', '', '' ... ''], please specify
   `skip_empty_rows=False` in order to preserve it. This becomes subtle when you
   try save a python dictionary where empty rows is not easy to be spotted.
#. `#69 <https://github.com/pyexcel/pyexcel/issues/69>`_: better documentation
   for save_book_as.

0.4.1 - 23.12.2016
--------------------------------------------------------------------------------

**Updated**

#. `#68 <https://github.com/pyexcel/pyexcel/issues/68>`_: regression
   save_to_memory() should have returned a stream instance.

0.4.0 - 22.12.2016
--------------------------------------------------------------------------------

**Added**

#. `Flask-Excel#19 <https://github.com/pyexcel/Flask-Excel/issues/19>`_ allow
   sheet_name parameter
#. `pyexcel-xls#11 <https://github.com/pyexcel/pyexcel-xls/issues/11>`_
   case-insensitive for file_type. `xls` and `XLS` are treated in the same way

**Updated**

#. `#66 <https://github.com/pyexcel/pyexcel/issues/66>`_: `export_columns` is
   ignored
#. Update dependency on pyexcel-io v0.3.0

0.3.3 - 07.11.2016
--------------------------------------------------------------------------------

**Updated**

#. `#63 <https://github.com/pyexcel/pyexcel/issues/63>`_: cannot display empty
   sheet(hence book with empty sheet) as texttable

0.3.2 - 02.11.2016
--------------------------------------------------------------------------------

**Updated**

#. `#62 <https://github.com/pyexcel/pyexcel/issues/62>`_: optional module import
   error become visible.

0.3.0 - 28.10.2016
--------------------------------------------------------------------------------

**Added:**

#. file type setters for Sheet and Book, and its documentation
#. `iget_records` returns a generator for a list of records and should have
   better memory performance, especially dealing with large csv files.
#. `iget_array` returns a generator for a list of two dimensional array and
   should have better memory performance, especially dealing with large csv
   files.
#. Enable pagination support, and custom row renderer via pyexcel-io v0.2.3

**Updated**

#. Take `isave_as` out from `save_as`. Hence two functions are there for save a
   sheet as
#. `#60 <https://github.com/pyexcel/pyexcel/issues/60>`_: encode 'utf-8' if the
   console is of ascii encoding.
#. `#59 <https://github.com/pyexcel/pyexcel/issues/59>`_: custom row renderer
#. `#56 <https://github.com/pyexcel/pyexcel/issues/56>`_: set cell value does
   not work
#. pyexcel.transpose becomes `pyexcel.sheets.transpose`
#. iterator functions of `pyexcel.Sheet` were converted to generator functions

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

#. `~pyexcel.Sheet.save_to_memory` and `~pyexcel.Book.save_to_memory` return the
   actual content. No longer they will return a io object hence you cannot call
   getvalue() on them.

**Removed:**

#. `content` and `out_file` as function parameters to the signature functions
   are no longer supported.
#. SourceFactory and RendererFactory are removed
#. The following methods are removed

   * `pyexcel.to_array`
   * `pyexcel.to_dict`
   * `pyexcel.utils.to_one_dimensional_array`
   * `pyexcel.dict_to_array`
   * `pyexcel.from_records`
   * `pyexcel.to_records`

#. `pyexcel.Sheet.filter` has been re-implemented and all filters were removed:

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

#. `pyexcel.Sheet.filter` has been re-implemented and all filters were removed:

   * pyexcel.formatters.SheetFormatter


0.2.5 - 31.08.2016
--------------------------------------------------------------------------------

**Updated:**

#. `#58 <https://github.com/pyexcel/pyexcel/issues/58>`_: texttable should have
   been made as compulsory requirement

0.2.4 - 14.07.2016
--------------------------------------------------------------------------------

**Updated:**

#. For python 2, writing to sys.stdout by pyexcel-cli raise IOError.

0.2.3 - 11.07.2016
--------------------------------------------------------------------------------

**Updated:**

#. For python 3, do not seek 0 when saving to memory if sys.stdout is passed on.
   Hence, adding support for sys.stdin and sys.stdout.

0.2.2 - 01.06.2016
--------------------------------------------------------------------------------

**Updated:**

#. Explicit imports, no longer needed
#. Depends on latest setuptools 18.0.1
#. NotImplementedError will be raised if parameters to core functions are not
   supported, e.g. get_sheet(cannot_find_me_option="will be thrown out as
   NotImplementedError")

0.2.1 - 23.04.2016
--------------------------------------------------------------------------------

**Added:**

#. add pyexcel-text file types as attributes of pyexcel.Sheet and pyexcel.Book,
   related to `#31 <https://github.com/pyexcel/pyexcel/issues/31>`__
#. auto import pyexcel-text if it is pip installed

**Updated:**

#. code refactoring done for easy addition of sources.
#. bug fix `#29 <https://github.com/pyexcel/pyexcel/issues/29>`__, Even if the
   format is a string it is displayed as a float
#. pyexcel-text is no longer a plugin to pyexcel-io but to pyexcel.sources, see
   `pyexcel-text#22 <https://github.com/pyexcel/pyexcel-text/issues/22>`__

**Removed:**

#. pyexcel.presentation is removed. No longer the internal decorate @outsource
   is used. related to `#31 <https://github.com/pyexcel/pyexcel/issues/31>`_

0.2.0 - 17.01.2016
--------------------------------------------------------------------------------

**Updated**

#. adopt pyexcel-io yield key word to return generator as content
#. pyexcel.save_as and pyexcel.save_book_as get performance improvements

0.1.7 - 03.07.2015
--------------------------------------------------------------------------------

**Added**

#. Support pyramid-excel which does the database commit on its own.

0.1.6 - 13.06.2015
--------------------------------------------------------------------------------

**Added**

#. get excel data from a http url

0.0.13 - 07.02.2015
--------------------------------------------------------------------------------

**Added**

#. Support django
#. texttable as default renderer

0.0.12 - 25.01.2015
--------------------------------------------------------------------------------

**Added**

#. Added sqlalchemy support

0.0.10 - 15.12.2015
--------------------------------------------------------------------------------

**Added**

#. added csvz and tsvz format

0.0.4 - 12.10.2014
--------------------------------------------------------------------------------

**Updated**

#. Support python 3

0.0.1 - 14.09.2014
--------------------------------------------------------------------------------

**Features:**

#. read and write csv, ods, xls, xlsx and xlsm files(which are referred later as
   excel files)
#. various iterators for the reader
#. row and column filters for the reader
#. utilities to get array and dictionary out from excel files.
#. cookbok receipes for some common and simple usage of this library.
