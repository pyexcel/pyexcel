import xlrd


DATE_FORMAT = "d"
FLOAT_FORMAT = "f"
INT_FORMAT = "i"
UNICODE_FORMAT = "u"
STRING_FORMAT = "s"
BOOLEAN_FORMAT = "b"
EMPTY = "e"


XLS_FORMAT_CONVERSION = {
    xlrd.XL_CELL_TEXT: STRING_FORMAT,
    xlrd.XL_CELL_EMPTY: EMPTY,
    xlrd.XL_CELL_DATE: DATE_FORMAT,
    xlrd.XL_CELL_NUMBER: FLOAT_FORMAT,
    xlrd.XL_CELL_BOOLEAN: INT_FORMAT,
    xlrd.XL_CELL_BLANK: EMPTY,
    xlrd.XL_CELL_ERROR: EMPTY
}


class Cell:
    def __init__(self, value_type, value):
        self.type = value_type
        self.value = value
