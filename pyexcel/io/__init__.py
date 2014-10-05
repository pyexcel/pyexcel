from odsbook import ODSBook, ODSWriter
from csvbook import CSVBook, CSVWriter
from xlbook import XLBook, XLWriter


"""
A list of registered readers
"""
READERS = {
    "xls": XLBook,
    "xlsm": XLBook,
    "xlsx": XLBook,
    "csv": CSVBook,
    "ods": ODSBook
}


"""
A list of registered writers
"""
WRITERS = {
    "xls": XLWriter,
    "xlsm": XLWriter,
    "xlsx": XLWriter,
    "csv": CSVWriter,
    "ods": ODSWriter
}


def load_file(file):
    extension = file.split(".")[-1]
    if extension in READERS:
        book_class = READERS[extension]
        book = book_class(file)
    else:
        raise NotImplementedError("can not open %s" % file)
    return book


def get_writer(file):
    extension = file.split(".")[-1]
    if extension in WRITERS:
        writer_class = WRITERS[extension]
        writer = writer_class(file)
        return writer
    else:
        raise NotImplementedError("Cannot open %s" % file)
        