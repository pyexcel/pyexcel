"""
    pyexcel.writers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for writing different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .utils import to_dict, to_array, from_records, dict_to_array
from .iterators import Matrix, transpose
from .io import get_writer
from .sheets import Sheet, IndexSheet


class SheetWriter:
    """Single sheet writer for the excel book writer"""

    def __init__(self, writer):
        """Constructor

        :param CustomWriter writer: format specific writer
        """
        self.writer = writer

    def write_array(self, table):
        """Write a two dimensional array

        :param list table: two dimensional array
        """
        self.write_rows(table)

    def write_rows(self, table):
        """
        Write a table

        table can be two dimensional array or a row iterator
        :param list table: two dimensional array        
        """
        if len(table) < 1:
            return
        rows = len(table)
        columns = len(table[0])
        self.writer.set_size((rows, columns))
        for row in table:
            self.writer.write_row(row)

    def write_dict(self, the_dict):
        """Write a dictionary
        
        :param dict the_dict: the dictionary to be writeen
        """
        array = dict_to_array(the_dict)
        self.write_rows(array)

    def write_reader(self, reader):
        """Write a reader/sheet

        :param Matrix reader: a Matrix instance
        """
        if not isinstance(reader, Matrix):
            raise TypeError
        if len(reader.rownames) > 0:
            self.write_dict(reader.to_dict(True))
        elif len(reader.colnames) > 0:
            self.write_dict(reader.to_dict())
        else:
            self.write_rows(to_array(reader))

    def write_columns(self, in_array):
        """Write columns in reference to rows

        It was seen always to write rows horizontally. This
        method write data vertically.
        :param list in_array: a two dimensional array
        """
        out_array = transpose(in_array)
        self.write_rows(out_array)

    def write_records(self, records):
        """Write records to rows

        key will become the column header and all data
        will be stacked one by one as rows
        :param list of dictionary records: the incoming data
        """
        out_array = from_records(records)
        self.write_rows(out_array)

    def close(self):
        """
        Close the writer

        Please remember to call close function
        """
        self.writer.close()


class BookWriter:
    """
    A generic book writer. 

    It provides one interface for writing any supported file formats. A book refers
    to the excel file that has many sheets. csv file format does not support such
    a concept, hence this writer will write a csv book in theory to scattered csv
    files which share similiar file names.
    """

    def __init__(self, file, **keywords):
        """Constructor
        :param str file: file name
        :param dict keywords: extra parameters for format specific writer
        """
        self.writer = get_writer(file, **keywords)

    def create_sheet(self, name):
        """Create a new sheet

        :param str name: the new sheet name
        """
        return SheetWriter(self.writer.create_sheet(name))

    def write_book_from_dict(self, sheet_dicts):
        """Write a dictionary to a multi-sheet file

        Requirements for the dictionary is: key is the sheet name,
        its value must be two dimensional array
        :param dict sheet_dicts: a dictionary of two dimensional array, for example::

            {
                "Sheet1": [[1, 2, 3], [4, 5, 6]],
                "Sheet2": [[7, 8, 9], [10, 11, 12]]
            }
        """
        keys = sheet_dicts.keys()
        for name in keys:
            sheet = self.create_sheet(name)
            sheet.write_array(sheet_dicts[name])
            sheet.close()

    def write_book_reader(self, bookreader):
        """
        Write a book reader

        Easy implementiation. Dump a book into a dictionary of two dimensional
        arrays. Then write book from this dictionary
        :param Book bookreader: a book object to be written
        """
        sheet_dicts = to_dict(bookreader)
        self.write_book_from_dict(sheet_dicts)

    def close(self):
        """close the writer"""
        self.writer.close()


class Writer(SheetWriter):
    """
    A single sheet excel file writer

    It writes only one sheet to an excel file. It is a quick way to handle most
    of the data files
    """

    def __init__(self, file, **keywords):
        """Constructor for single sheet writer

        This class creates only one sheet writer and stick with it
        """
        self.bookwriter = BookWriter(file, **keywords)
        self.writer = self.bookwriter.create_sheet(None).writer

    def close(self):
        """
        Close the writer
        """
        SheetWriter.close(self)
        self.bookwriter.close()
