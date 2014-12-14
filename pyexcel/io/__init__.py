"""
    pyexcel.io
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading/writing different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from functools import partial
from .csvbook import CSVBook, CSVWriter
from .csvzipbook import CSVZipWriter, CSVZipBook
from .._compact import is_string


# A list of registered readers
READERS = {
    "csv": CSVBook,
    "tsv": partial(CSVBook, dialect="excel-tab"),
    "csvz": CSVZipBook,
    "tsvz": partial(CSVZipBook, dialect="excel-tab")
}


# A list of registered writers
WRITERS = {
    "csv": CSVWriter,
    "tsv": partial(CSVWriter, dialect="excel-tab"),
    "csvz": CSVZipWriter,
    "tsvz": partial(CSVZipWriter, dialect="excel-tab")
}


def list_readers():
    """list available readers"""
    print(READERS.keys())


def list_writers():
    """list available writers"""
    print(WRITERS.keys())


def load_file(filename, **keywords):
    """Load data from any supported excel formats
    """
    extension = None
    if isinstance(filename, tuple):
        extension = filename[0]
        content = filename[1]
        if extension in READERS:
            book_class = READERS[extension]
            book = book_class(None, file_content=content, **keywords)
        else:
            raise NotImplementedError("can not open %s stream" % filename[0])
    elif is_string(type(filename)):
        extension = filename.split(".")[-1]
        if extension in READERS:
            book_class = READERS[extension]
            book = book_class(filename, **keywords)
        else:
            raise NotImplementedError("can not open %s" % filename)
    else:
        raise IOError("cannot handle unknown content")
    return book


def get_writer(filename, **keywords):
    """Create a writer from any supported excel formats
    """
    extension = None
    if isinstance(filename, tuple):
        extension = filename[0]
        if extension in WRITERS:
            writer_class = WRITERS[extension]
            writer = writer_class(filename[1], **keywords)
            return writer
        else:
            raise NotImplementedError("Cannot write %s stream" % filename[0])
    elif is_string(type(filename)):
        extension = filename.split(".")[-1]
        if extension in WRITERS:
            writer_class = WRITERS[extension]
            writer = writer_class(filename, **keywords)
            return writer
        else:
            raise NotImplementedError("Cannot open %s" % filename)
    else:
        raise IOError("cannot handle unknown content")
