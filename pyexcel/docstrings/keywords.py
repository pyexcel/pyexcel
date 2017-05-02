CSV_PARAMS = """
**CSV format specifi parameters**

delimiter : csv specific, field separator

lineterminator : csv specific, line terminator
"""

OPTIONAL_PARAMS = """
auto_detect_float : defaults to True

auto_detect_int : defaults to True

auto_detect_datetime : defaults to True

ignore_infinity : defaults to True

library : choose a specific pyexcel-io plugin for reading

source_library : choose a specific data source plugin for reading

parser_library : choose a pyexcel parser plugin for reading
"""

FILE_PARAMS = """
file_name : a file with supported file extension

file_content : the file content

file_stream : the file stream

file_type : the file type in *file_content* or *file_stream*
"""

SOURCE_PARAMS = """

**Parameters**

""" + FILE_PARAMS + """
session : database session

table : database table

model: a django model

adict: a dictionary of one dimensional arrays

url : a download http url for your excel file

with_keys : load with previous dictionary's keys, default is True

records : a list of dictionaries that have the same keys

array : a two dimensional array, a list of lists

sheet_name : sheet name. if sheet_name is not given, the default
sheet at index 0 is loaded

""" + OPTIONAL_PARAMS + CSV_PARAMS

SOURCE_PARAMS_TABLE = """
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

DEST_PARAMS = """
dest_file_name: another file name.

dest_file_type: this is needed if you want to save to memory

dest_session: the target database session

dest_table: the target destination table

dest_model: the target django model

dest_mapdict: a mapping dictionary
    see :meth:`pyexcel.Sheet.save_to_memory`

dest_initializer: a custom initializer function for table or model

dest_mapdict: nominate headers

dest_batch_size: object creation batch size.
     it is Django specific
dest_library: choose a specific pyexcel-io plugin for writing

dest_source_library: choose a specific data source plugin for writing

deset_renderer_library: choose a pyexcel parser plugin for writing
"""

SOURCE_BOOK_PARAMS = FILE_PARAMS + """
session : database session

tables : a list of database table

models : a list of django models

bookdict : a dictionary of two dimensional arrays

url : a download http url for your excel file
""" + OPTIONAL_PARAMS + CSV_PARAMS

SOURCE_BOOK_PARAMS_TABLE = """
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

Where the dictionary should have text as keys and two dimensional
array as values.
"""
