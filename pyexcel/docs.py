__SOURCE_KEYWORDS__ = """
:param file_name: a file with supported file extension
:param file_content: the file content
:param file_stream: the file stream
:param file_type: the file type in *content*
:param session: database session
:param table: database table
:param model: a django model
:param adict: a dictionary of one dimensional arrays
:param url: a download http url for your excel file
:param with_keys: load with previous dictionary's keys, default is True
:param records: a list of dictionaries that have the same keys
:param array: a two dimensional array, a list of lists
:param keywords: additional parameters, see :meth:`Sheet.__init__`
:param sheet_name: sheet name. if sheet_name is not given,
                   the default sheet at index 0 is loaded
"""

__SOURCE_KEYWORDS_TABLE__ = """
Not all parameters are needed. Here is a table

========================== =========================================
source                     parameters
========================== =========================================
loading from file          file_name, sheet_name, keywords
loading from string        file_content, file_type, sheet_name, keywords
loading from stream        file_stream, file_type, sheet_name, keywords
loading from sql           session, table
loading from sql in django model
loading from query sets    any query sets(sqlalchemy or django)
loading from dictionary    adict, with_keys
loading from records       records
loading from array         array
loading from an url        url
========================== =========================================
"""

__DEST_KEYWORDS__ = """
:param dest_file_name: another file name. **out_file** is deprecated
                       though is still accepted.
:param dest_file_type: this is needed if you want to save to memory
:param dest_session: the target database session
:param dest_table: the target destination table
:param dest_model: the target django model
:param dest_mapdict: a mapping dictionary,
                     see :meth:`pyexcel.Sheet.save_to_memory`
:param dest_initializer: a custom initializer function for table or model
:param dest_mapdict: nominate headers
:param dest_batch_size: object creation batch size.
                        it is Django specific
"""

GET_SHEET_DOC = """
Get an instance of :class:`Sheet` from an excel source
""" + __SOURCE_KEYWORDS__ + __SOURCE_KEYWORDS_TABLE__

GET_ARRAY_DOC = """
Obtain an array from an excel source

It accepts the same parameters as :meth:`~pyexcel.get_sheet`
but return an array instead.
""" + __SOURCE_KEYWORDS__ + __SOURCE_KEYWORDS_TABLE__

IGET_ARRAY_DOC = """
Obtain a generator of an two dimensional array from an excel source

It is similiar to :meth:`pyexcel.get_array` but it has less memory
footprint.
""" + __SOURCE_KEYWORDS__ + __SOURCE_KEYWORDS_TABLE__

GET_DICT_DOC = """
Obtain a dictionary from an excel source

It accepts the same parameters as :meth:`~pyexcel.get_sheet`
but return a dictionary instead.

Specifically:
:param name_columns_by_row: specify a row to be a dictionary key.
It is default to 0 or first row.

If you would use a column index 0 instead, you should do::

    get_dict(name_columns_by_row=-1, name_rows_by_column=0)

""" + __SOURCE_KEYWORDS__ + __SOURCE_KEYWORDS_TABLE__


GET_RECORDS_DOC = """
Obtain a list of records from an excel source

It accepts the same parameters as :meth:`~pyexcel.get_sheet`
but return a list of dictionary(records) instead.

Specifically:
:param name_columns_by_row: specify a row to be a dictionary key.
It is default to 0 or first row.

If you would use a column index 0 instead, you should do::

    get_records(name_columns_by_row=-1, name_rows_by_column=0)

""" + __SOURCE_KEYWORDS__ + __SOURCE_KEYWORDS_TABLE__

IGET_RECORDS_DOC = """
Obtain a generator of a list of records from an excel source

It is similiar to :meth:`pyexcel.get_records` but it has less memory
footprint but requires the headers to be in the first row. And the
data matrix should be of equal length. It should consume less memory
and should work well with large files.
""" + __SOURCE_KEYWORDS__ + __SOURCE_KEYWORDS_TABLE__

__SOURCE_BOOK_KEYWORDS__ = """
:param file_name: a file with supported file extension
:param file_content: the file content
:param file_stream: the file stream
:param file_type: the file type in *content*
:param session: database session
:param tables: a list of database table
:param models: a list of django models
:param bookdict: a dictionary of two dimensional arrays
:param url: a download http url for your excel file
"""

__SOURCE_BOOK_KEYWORDS_TABLE__ = """
Here is a table of parameters:

========================== ===============================
source                     parameters
========================== ===============================
loading from file          file_name, keywords
loading from string        file_content, file_type, keywords
loading from stream        file_stream, file_type, keywords
loading from sql           session, tables
loading from django models models
loading from dictionary    bookdict
loading from an url        url
========================== ===============================
"""

GET_BOOK_DOC = """
Get an instance of :class:`Book` from an excel source

""" + __SOURCE_BOOK_KEYWORDS__ + """

see also :ref:`a-list-of-data-structures`

""" + __SOURCE_BOOK_KEYWORDS_TABLE__ + """

Where the dictionary should have text as keys and two dimensional
array as values.
"""

GET_BOOK_DICT_DOC = """
Obtain a dictionary of two dimensional arrays

It accepts the same parameters as :meth:`~pyexcel.get_book`
but return a dictionary instead.
""" + __SOURCE_BOOK_KEYWORDS__ + __SOURCE_BOOK_KEYWORDS_TABLE__ + """

Where the dictionary should have text as keys and two dimensional
array as values.
"""


SAVE_AS_DOC = """
Save a sheet from a data source to another one

It accepts two sets of keywords. Why two sets? one set is
source, the other set is destination. In order to distinguish
the two sets, source set will be exactly the same
as the ones for :meth:`pyexcel.get_sheet`; destination
set are exactly the same as the ones for :class:`pyexcel.Sheet.save_as`
but require a 'dest' prefix.
""" + (
    __SOURCE_KEYWORDS__ +
    __DEST_KEYWORDS__
) + """
:returns: IO stream if saving to memory. None otherwise

if csv file is destination format, python csv
`fmtparams <https://docs.python.org/release/3.1.5/
library/csv.html#dialects-and-formatting-parameters>`_
are accepted

for example: dest_lineterminator will replace default '\r\n'
to the one you specified

""" + __SOURCE_KEYWORDS_TABLE__ + """

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

SAVE_BOOK_AS_DOC = """
Save a book from a data source to another one
""" + __SOURCE_BOOK_KEYWORDS__ + """
:param dest_file_name: another file name. **out_file** is
                       deprecated though is still accepted.
:param dest_file_type: this is needed if you want to save to memory
:param dest_session: the target database session
:param dest_tables: the list of target destination tables
:param dest_models: the list of target destination django models
:param dest_mapdicts: a list of mapping dictionaries
:param dest_initializers: table initialization functions
:param dest_mapdicts: to nominate a model or table fields. Optional
:param dest_batch_size: batch creation size. Optional
:param keywords: additional keywords can be found at
                 :meth:`pyexcel.get_book`
:returns: IO stream if saving to memory. None otherwise


see also :ref:`a-list-of-data-structures`
""" + __SOURCE_BOOK_KEYWORDS_TABLE__ + """

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
