"""
    pyexcel.writers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for writing different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from utils import to_dict
from readers import SeriesReader
from io import get_writer


class SheetWriter:
    """Single sheet writer for the excel book writer"""

    def __init__(self, writer):
        self.writer = writer

    def write_row(self, array):
        """
        Write a row

        write a row into the file in memory
        """
        self.writer.write_row(array)

    def write_array(self, table):
        self.write_rows(table)

    def write_rows(self, table):
        """
        Write a table

        table can be two dimensional array or a row iterator
        """
        for row in table:
            self.writer.write_row(row)

    def write_columns(self, table):
        max_length = -1
        for c in table:
            column_length = len(c)
            if max_length == -1:
                max_length = column_length
            elif max_length < column_length:
                max_length = column_length
        for i in range(0, max_length):
            row_data = []
            for c in table:
                if i < len(c):
                    row_data.append(c[i])
                else:
                    row_data.append('')
            self.writer.write_row(row_data)

    def write_dict(self, the_dict, with_headers=True):
        """
        Write a whole dictionary

        series and data will be write into one file
        """
        keys = sorted(the_dict.keys())
        if with_headers:
            self.writer.write_row(keys)
        max_length = -1
        for k in keys:
            column_length = len(the_dict[k])
            if max_length == -1:
                max_length = column_length
            elif max_length < column_length:
                max_length = column_length
        for i in range(0, max_length):
            row_data = []
            for k in keys:
                if i < len(the_dict[k]):
                    row_data.append(the_dict[k][i])
                else:
                    row_data.append('')
            self.writer.write_row(row_data)

    def write_reader(self, reader):
        """
        Write a pyexcel reader

        In this case, you may use FiterableReader or SeriesReader
        to do filtering first. Then pass it onto this function
        """
        if isinstance(reader, SeriesReader):
            self.write_dict(to_dict(reader))
        else:
            self.write_array(reader.rows())

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

    It writes only one sheet to an exce file. It is a quick way to handle most
    of the data files
    """

    def __init__(self, file):
        self.bookwriter = BookWriter(file)
        self.writer = self.bookwriter.create_sheet(None).writer

    def close(self):
        SheetWriter.close(self)
        self.bookwriter.close()
