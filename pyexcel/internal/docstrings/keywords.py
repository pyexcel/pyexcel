CSV_PARAMS = """
**Parameters related to csv file format**

delimiter :
    csv specific, field separator

lineterminator :
    csv specific, line terminator

encoding:
    csv specific. Specify the file encoding the csv file. For example:
    encoding='latin1'. Especially, encoding='utf-8-sig' would add utf 8
    bom header if used in renderer, or would parse a csv with utf brom header
    used in parser.
"""

XLRD_PARAMS = """
**Parameters related to xls file format:**
    Please note the following parameters apply to pyexcel-xls.
    more details can be found in :func:`xlrd.open_workbook`

logfile:
    An open file to which messages and diagnostics are written.

verbosity:
    Increases the volume of trace material written to the logfile.

use_mmap:
    Whether to use the mmap module is determined heuristically.
    Use this arg to override the result.

    Current heuristic: mmap is used if it exists.

encoding_override:
     Used to overcome missing or bad codepage information
     in older-version files.

formatting_info:
     The default is False, which saves memory.

     When True, formatting information will be read from the spreadsheet
     file. This provides all cells, including empty and blank cells.
     Formatting information is available for each cell.

ragged_rows:
     The default of False means all rows are padded out with empty
     cells so that all rows have the same size as found in ncols.

     True means that there are no empty cells at the ends of rows. This
     can result in substantial memory savings if rows are of widely
     varying sizes. See also the row_len() method.
"""

OPTIONAL_PARAMS = """
auto_detect_float :
    defaults to True

auto_detect_int :
    defaults to True

auto_detect_datetime :
    defaults to True

ignore_infinity :
    defaults to True

library :
    choose a specific pyexcel-io plugin for reading

source_library :
    choose a specific data source plugin for reading

parser_library :
    choose a pyexcel parser plugin for reading

skip_hidden_sheets:
     default is True. Please toggle it to read hidden sheets

"""

FILE_PARAMS = """
file_name :
    a file with supported file extension

file_content :
    the file content

file_stream :
    the file stream

file_type :
     the file type in *file_content* or *file_stream*
"""

SKIPPING_FUNC_PROTOCOL = """
    The protocol is
    to return pyexcel_io.constants.SKIP_DATA if skipping data,
    pyexcel_io.constants.TAKE_DATA to read data,
    pyexcel_io.constants.STOP_ITERATION to exit the reading procedure
"""

PAGINATION_PARAMS = """
start_row : int
    defaults to 0. It allows you to skip rows at the begginning

row_limit: int
    defaults to -1, meaning till the end of the whole sheet. It allows
    you to skip the tailing rows.

start_column : int
    defaults to 0. It allows you to skip columns on your left hand side

column_limit: int
    defaults to -1, meaning till the end of the columns. It allows
    you to skip the tailing columns.

skip_row_func:
    It allows you to write your own row skipping functions.
""" + SKIPPING_FUNC_PROTOCOL + """
skip_column_func:
    It allows you to write your own column skipping functions.
""" + SKIPPING_FUNC_PROTOCOL + """
skip_empty_rows: bool
    Defaults to False. Toggle it to True if the rest of empty rows are
    useless, but it does affect the number of rows.

row_renderer:
    You could choose to write a custom row renderer when the data is being
    read.
"""

SOURCE_PARAMS = FILE_PARAMS + """
session :
    database session

table :
    database table

model:
    a django model

adict:
    a dictionary of one dimensional arrays

url :
    a download http url for your excel file

with_keys :
    load with previous dictionary's keys, default is True

records :
    a list of dictionaries that have the same keys

array :
    a two dimensional array, a list of lists

sheet_name :
    sheet name. if sheet_name is not given, the default
    sheet at index 0 is loaded

sheets:
    a list of mixed sheet names and sheet indices to be read. This is
    done to keep Pandas compactibility. With this parameter, more than
    one sheet can be read and you have the control to read the sheets
    of your interest instead of all available sheets.

""" + PAGINATION_PARAMS + OPTIONAL_PARAMS + CSV_PARAMS + XLRD_PARAMS

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

DEST_FILE_PARAMS = """
dest_file_name:
    another file name.

dest_file_type:
    this is needed if you want to save to memory
"""

DEST_PARAMS = DEST_FILE_PARAMS + """
dest_session:
    the target database session

dest_table:
    the target destination table

dest_model:
    the target django model

dest_mapdict:
    a mapping dictionary
    see :meth:`pyexcel.Sheet.save_to_memory`

dest_initializer:
    a custom initializer function for table or model

dest_mapdict:
    nominate headers

dest_batch_size:
    object creation batch size.
    it is Django specific

dest_library:
    choose a specific pyexcel-io plugin for writing

dest_source_library:
    choose a specific data source plugin for writing

dest_renderer_library:
    choose a pyexcel parser plugin for writing
"""

DEST_PARAMS_TABLE = """
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
"""

DEST_BOOK_PARAMS = DEST_FILE_PARAMS + """
dest_session :
    the target database session

dest_tables :
    the list of target destination tables

dest_models :
    the list of target destination django models

dest_mapdicts :
    a list of mapping dictionaries

dest_initializers :
    table initialization functions

dest_mapdicts :
    to nominate a model or table fields. Optional

dest_batch_size :
    batch creation size. Optional
"""

SOURCE_BOOK_PARAMS = FILE_PARAMS + """
session :
    database session

tables :
    a list of database table

models :
    a list of django models

bookdict :
    a dictionary of two dimensional arrays

url :
    a download http url for your excel file
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
