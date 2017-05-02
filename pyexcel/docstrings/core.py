from . import keywords

__GET_SHEET__ = keywords.SOURCE_PARAMS_TABLE + keywords.SOURCE_PARAMS

GET_SHEET = """
Get an instance of :class:`Sheet` from an excel source
""" + __GET_SHEET__

GET_ARRAY = """
Obtain an array from an excel source

It accepts the same parameters as :meth:`~pyexcel.get_sheet`
but return an array instead.
""" + __GET_SHEET__

IGET_ARRAY = """
Obtain a generator of an two dimensional array from an excel source

It is similiar to :meth:`pyexcel.get_array` but it has less memory
footprint.
""" + __GET_SHEET__

GET_DICT = """
Obtain a dictionary from an excel source

It accepts the same parameters as :meth:`~pyexcel.get_sheet`
but return a dictionary instead.

Specifically:
name_columns_by_row : specify a row to be a dictionary key.
It is default to 0 or first row.

If you would use a column index 0 instead, you should do::

    get_dict(name_columns_by_row=-1, name_rows_by_column=0)

""" + __GET_SHEET__

GET_RECORDS = """
Obtain a list of records from an excel source

It accepts the same parameters as :meth:`~pyexcel.get_sheet`
but return a list of dictionary(records) instead.

Specifically:
name_columns_by_row : specify a row to be a dictionary key.
It is default to 0 or first row.

If you would use a column index 0 instead, you should do::

    get_records(name_columns_by_row=-1, name_rows_by_column=0)

""" + __GET_SHEET__

IGET_RECORDS = """
Obtain a generator of a list of records from an excel source

It is similiar to :meth:`pyexcel.get_records` but it has less memory
footprint but requires the headers to be in the first row. And the
data matrix should be of equal length. It should consume less memory
and should work well with large files.
""" + __GET_SHEET__

__SAVE_AS__ = """
It accepts two sets of keywords. Why two sets? one set is
source, the other set is destination. In order to distinguish
the two sets, source set will be exactly the same
as the ones for :meth:`pyexcel.get_sheet`; destination
set are exactly the same as the ones for :class:`pyexcel.Sheet.save_as`
but require a 'dest' prefix.
""" + __GET_SHEET__ + """
:returns: IO stream if saving to memory. None otherwise

if csv file is destination format, python csv
`fmtparams <https://docs.python.org/release/3.1.5/
library/csv.html#dialects-and-formatting-parameters>`_
are accepted

for example: dest_lineterminator will replace default '\r\n'
to the one you specified

""" + keywords.SOURCE_PARAMS_TABLE + """

================= =============================================
Saving to source  parameters
================= =============================================
file              dest_file_name, dest_sheet_name,
                  keywords with prefix 'dest'
memory            dest_file_type, dest_content,
                  dest_sheet_name, keywords with prefix 'dest'
sql               dest_session, dest_table,
                  dest_initializer, dest_mapdict
django model      dest_model, dest_initializer,
                  dest_mapdict, dest_batch_size
================= =============================================

In addition, this function use :class:`pyexcel.Sheet` to
render the data which could have performance penalty. In exchange,
parameters for :class:`pyexcel.Sheet` can be passed on, e.g.
`name_columns_by_row`.

"""

SAVE_AS = """
Save a sheet from a data source to another one
""" + __SAVE_AS__

ISAVE_AS = """
Save a sheet from a data source to another one with less memory

It is simliar to :meth:`pyexcel.save_as` except that it does
not accept parameters for :class:`pyexcel.Sheet`. And it read
when it writes.
""" + __SAVE_AS__

__GET_BOOK__ = keywords.SOURCE_BOOK_PARAMS_TABLE + keywords.SOURCE_BOOK_PARAMS

GET_BOOK = """
Get an instance of :class:`Book` from an excel source

""" + __GET_BOOK__

GET_BOOK_DICT = """
Obtain a dictionary of two dimensional arrays

It accepts the same parameters as :meth:`~pyexcel.get_book`
but return a dictionary instead.
""" + __GET_BOOK__

__SAVE_BOOK_AS__ = """
""" + keywords.SOURCE_BOOK_PARAMS + """
dest_file_name : another file name. **out_file** is
                deprecated though is still accepted.

dest_file_type : this is needed if you want to save to memory

dest_session: the target database session

dest_tables : the list of target destination tables

dest_models : the list of target destination django models

dest_mapdicts : a list of mapping dictionaries

dest_initializers: table initialization functions

dest_mapdicts : to nominate a model or table fields. Optional

dest_batch_size : batch creation size. Optional

keywords : additional keywords can be found at :meth:`pyexcel.get_book`

returns : IO stream if saving to memory. None otherwise


see also :ref:`a-list-of-data-structures`
""" + keywords.SOURCE_BOOK_PARAMS_TABLE + """

Where the dictionary should have text as keys and two dimensional
array as values.

================ ============================================
Saving to source parameters
================ ============================================
file             dest_file_name, dest_sheet_name,
                 keywords with prefix 'dest'
memory           dest_file_type, dest_content,
                 dest_sheet_name, keywords with prefix 'dest'
sql              dest_session, dest_tables,
                 dest_table_init_func, dest_mapdict
django model     dest_models, dest_initializers,
                 dest_mapdict, dest_batch_size
================ ============================================
"""

SAVE_BOOK_AS = """
Save a book from a data source to another one
""" + __SAVE_BOOK_AS__

ISAVE_BOOK_AS = """
Save a book from a data source to another one

It is simliar to :meth:`pyexcel.save_book_as` but it read
when it writes. This function provide some speedup but
the output data is not made uniform.
""" + __SAVE_BOOK_AS__
