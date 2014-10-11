"""
    pyexcel.writers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for writing different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .utils import to_dict, dict_to_array, transpose
from .iterators import Matrix
from .io import get_writer


class SheetWriter:
    """Single sheet writer for the excel book writer"""

    def __init__(self, writer):
        self.writer = writer

    def write_array(self, table):
        self.write_rows(table)

    def write_rows(self, table):
        """
        Write a table

        table can be two dimensional array or a row iterator
        """
        if len(table) < 1:
            return
        columns = len(table)
        rows = len(table[0])
        self.writer.set_size((columns, rows))
        for row in table:
            self.writer.write_row(row)

    def write_dict(self, the_dict):
        array = dict_to_array(the_dict)
        self.write_rows(array)

    def write_reader(self, reader):
        if isinstance(reader, Matrix):
            self.write_rows(reader.array)
        else:
            raise TypeError

    def write_columns(self, in_array):
        out_array = transpose(in_array)
        self.write_rows(out_array)

    def close(self):
        """
        Close the writer

        Please remember to call close function
        """
        self.writer.close()


class BookWriter:
    """
    A generic book writer

    It provides one interface for writing ods, csv, xls, xlsx and xlsm
    """

    def __init__(self, file):
        self.writer = get_writer(file)

    def create_sheet(self, name):
        return SheetWriter(self.writer.create_sheet(name))

    def write_book_from_dict(self, sheet_dicts):
        """Write a dictionary to a multi-sheet file

        Requirements for the dictionary is: key is the sheet name,
        its value must be two dimensional array
        """
        keys = sheet_dicts.keys()
        for name in keys:
            sheet = self.create_sheet(name)
            sheet.write_array(sheet_dicts[name])
            sheet.close()

    def write_book_reader(self, bookreader):
        """
        Write a book reader
        """
        sheet_dicts = to_dict(bookreader)
        self.write_book_from_dict(sheet_dicts)

    def close(self):
        self.writer.close()


class Writer(SheetWriter):
    """
    A single sheet excel file writer

    It writes only one sheet to an excel file. It is a quick way to handle most
    of the data files
    """

    def __init__(self, file):
        self.bookwriter = BookWriter(file)
        self.writer = self.bookwriter.create_sheet(None).writer

    def close(self):
        SheetWriter.close(self)
        self.bookwriter.close()
