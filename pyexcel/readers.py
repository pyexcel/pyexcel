"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from ext.odsbook import ODSBook
from ext.csvbook import CSVBook
from ext.xlbook import XLBook
from iterators import (HBRTLIterator,
                       HTLBRIterator,
                       VBRTLIterator,
                       VTLBRIterator,
                       RowIterator,
                       RowReverseIterator,
                       ColumnIterator,
                       ColumnReverseIterator,
                       SeriesColumnIterator,
                       SheetIterator)
from common import RawSheet, PlainSheet, MultipleFilterableSheet, Sheet



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


class BookReader:
    """
    Read an excel book that has mutliple sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, file):
        """
        Book constructor

        Selecting a specific book according to file extension
        """
        extension = file.split(".")[-1]
        if extension in READERS:
            book_class = READERS[extension]
            book = book_class(file)
        else:
            raise NotImplementedError("can not open %s" % file)
        self.sheets = book.sheets()
        self.name_array = self.sheets.keys()

    def __iter__(self):
        return SheetIterator(self)

    def number_of_sheets(self):
        """Return the number of sheets"""
        return len(self.name_array)

    def sheet_names(self):
        """Return all sheet names"""
        return self.name_array

    def sheet_by_name(self, name):
        """Get the sheet with the specified name"""
        return self.sheets[name]

    def sheet_by_index(self, index):
        """Get the sheet with the specified index"""
        if index < len(self.name_array):
            sheet_name = self.name_array[index]
            return self.sheets[sheet_name]

    def __getitem__(self, key):
        if type(key) == int:
            return self.sheet_by_index(key)
        else:
            return self.sheet_by_name(key)


class Reader(Sheet):
    """
    A single sheet excel file reader

    Default is the sheet at index 0. Or you specify one using sheet index
    or sheet name. The short coming of this reader is: column filter is
    applied first then row filter is applied next
    """

    def __init__(self, file, sheet=None):
        self.book = BookReader(file)
        if sheet:
            Sheet.__init__(self, self.book[sheet].sheet, self.book[sheet].name)
        else:
            Sheet.__init__(self, self.book[0].sheet, self.book[0].name)


class SeriesReader(Reader):
    """
    A single sheet excel file reader and it has column headers
    """

    def __init__(self, file, sheet=None):
        Reader.__init__(self, file, sheet)
        self.become_series()


class PlainReader(PlainSheet):
    """
    PlainReader exists for speed over Reader and also for testing purposes
    """
    def __init__(self, file, sheet=None):
        self.book = BookReader(file)
        if sheet:
            PlainSheet.__init__(self, self.book[sheet].sheet)
        else:
            PlainSheet.__init__(self, self.book[0].sheet)


class FilterableReader(MultipleFilterableSheet):
    """
    FiltableReader lets you use filters at the sequence of your choice
    """
    def __init__(self, file, sheet=None):
        self.book = BookReader(file)
        if sheet:
            MultipleFilterableSheet.__init__(self, self.book[sheet].sheet)
        else:
            MultipleFilterableSheet.__init__(self, self.book[0].sheet)
