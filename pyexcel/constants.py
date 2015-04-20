"""
    pyexcel.constants
    ~~~~~~~~~~~~~~~~~~~

    Constants appeared in pyexcel

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
DEFAULT_NAME = 'pyexcel'
DEFAULT_SHEET_NAME = 'pyexcel_sheet1'

MESSAGE_WARNING = "We do not overwrite files"
MESSAGE_WRITE_ERROR = "Cannot write sheet"
MESSAGE_INVALID_PARAMETERS = "Invalid parameters"
MESSAGE_ERROR_02 = "No valid parameters found!"
MESSAGE_ERROR_03 = "cannot handle unknown content"
MESSAGE_DATA_ERROR_NO_SERIES = "No column names or row names found"
MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST = "Column list is empty. Do not waste resource"
MESSAGE_DATA_ERROR_COLUMN_LIST_INTEGER_TYPE = "Column list should be a list of integers"
MESSAGE_DATA_ERROR_COLUMN_LIST_STRING_TYPE = "Column list should be a list of integers"
MESSAGE_INDEX_OUT_OF_RANGE = "Index out of range"
MESSAGE_DATA_ERROR_EMPTY_CONTENT = "Nothing to be pasted!"
MESSAGE_DATA_ERROR_DATA_TYPE_MISMATCH = "Data type mismatch"
MESSAGE_DATA_ERROR_ORDEREDDICT_IS_EXPECTED = "Please give a ordered list"

MESSAGE_DEPRECATED_ROW_COLUMN = "Deprecated usage. Please use [row, column]"
MESSAGE_DEPRECATED_02 = "Depreciated usage. please use dest_file_name"

MESSAGE_NOT_IMPLEMENTED_01 = "Please use attribute row or column to extend sheet"
MESSAGE_NOT_IMPLEMENTED_02 = "Confused! What do you want to put as column names"
MESSAGE_CANNOT_WRITE_STREAM_FORMATTER = "Cannot write content of file type %s to stream"
MESSAGE_CANNOT_READ_STREAM_FORMATTER = "Cannot read content of file type %s from stream"
MESSAGE_CANNOT_WRITE_FILE_TYPE_FORMATTER = "Cannot write content of file type %s to file %s"
MESSAGE_CANNOT_READ_FILE_TYPE_FORMATTER = "Cannot read content of file type %s from file %s"
MESSAGE_LOADING_FORMATTER = "The plugin for file type %s is not installed. Please install %s"


# Used by sources
KEYWORD_MEMORY = 'memory'
KEYWORD_SOURCE = 'source'
KEYWORD_FILE_TYPE = 'file_type'
KEYWORD_FILE_NAME = 'file_name'
KEYWORD_SESSION = 'session'
KEYWORD_TABLE = 'table'
KEYWORD_MODEL = 'model'
KEYWORD_TABLES = 'tables'
KEYWORD_MODELS = 'models'
KEYWORD_CONTENT = 'content'
KEYWORD_ADICT = 'adict'
KEYWORD_RECORDS = 'records'
KEYWORD_ARRAY = 'array'
KEYWORD_COLUMN_NAMES = 'column_names'
KEYWORD_QUERY_SETS = 'query_sets'
KEYWORD_OUT_FILE = 'out_file'
KEYWORD_BOOKDICT = 'bookdict'
KEYWORD_MAPDICT = 'mapdict'
KEYWORD_MAPDICTS = 'mapdicts'
KEYWORD_INITIALIZER = 'initializer'
KEYWORD_INITIALIZERS = 'initializers'
KEYWORD_BATCH_SIZE = 'batch_size'

KEYWORD_STARTS_WITH_DEST = '^dest_(.*)'
