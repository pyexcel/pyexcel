"""
    pyexcel.writers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for writing different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from utils import to_dict
from readers import SeriesReader


class ODSSheetWriter:
    """
    ODS sheet writer
    """
    
    def __init__(self, book, name):
        from odf.table import Table
        self.doc = book
        if name:
            sheet_name = name
        else:
            sheet_name = "pyexcel_sheet1"
        self.table = Table(name=sheet_name)

    def write_row(self, array):
        """
        write a row into the file
        """
        from odf.table import TableRow, TableCell
        from odf.text import P
        tr = TableRow()
        self.table.addElement(tr)
        for x in array:
            tc = TableCell()
            tc.addElement(P(text=x))
            tr.addElement(tc)

    def close(self):
        """
        This call writes file
        
        """
        self.doc.spreadsheet.addElement(self.table)


class ODSWriter:
    """
    open document spreadsheet writer
    
    """
    def __init__(self, file):
        from odf.opendocument import OpenDocumentSpreadsheet
        self.doc = OpenDocumentSpreadsheet()
        self.file = file

    def create_sheet(self, name):
        """
        write a row into the file
        """
        return ODSSheetWriter(self.doc, name)

    def close(self):
        """
        This call writes file
        
        """
        self.doc.write(self.file)


class CSVSheetWriter:
    """
    csv file writer
    
    """
    def __init__(self, file, name):
        import csv
        if name:
            names = file.split(".")
            file_name = "%s_%s.%s" % (names[0], name, names[1])
        else:
            file_name = file

        self.f = open(file_name, "wb")
        self.writer = csv.writer(self.f)

    def write_row(self, array):
        """
        write a row into the file
        """
        self.writer.writerow(array)

    def close(self):
        """
        This call close the file handle
        """
        self.f.close()

        
class CSVWriter:
    """
    csv file writer

    if there is multiple sheets for csv file, it simpily writes
    multiple csv files
    """
    def __init__(self, file):
        self.file = file
        self.count = 0

    def create_sheet(self, name):
        return CSVSheetWriter(self.file, name)

    def close(self):
        """
        This call close the file handle
        """
        pass


class XLSSheetWriter:
    """
    xls, xlsx and xlsm sheet writer
    """
    def __init__(self, wb, name):
        self.wb = wb
        if name:
            sheet_name = name
        else:
            sheet_name = "pyexcel_sheet1"
        self.ws = self.wb.add_sheet(sheet_name)
        self.current_row = 0

    def write_row(self, array):
        """
        write a row into the file
        """
        for i in range(0, len(array)):
            self.ws.write(self.current_row, i, array[i])
        self.current_row += 1

    def close(self):
        """
        This call actually save the file
        """
        pass


class XLSWriter:
    """
    xls, xlsx and xlsm writer
    """
    def __init__(self, file):
        import xlwt
        self.file = file
        self.wb = xlwt.Workbook()
        self.current_row = 0

    def create_sheet(self, name):
        return XLSSheetWriter(self.wb, name)

    def close(self):
        """
        This call actually save the file
        """
        self.wb.save(self.file)


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
        """
        Write a table

        table can be two dimensional array or a row iterator
        """
        for row in table:
            self.writer.write_row(row)

    def write_dict(self, the_dict):
        """
        Write a whole dictionary

        series and data will be write into one file
        """
        keys = sorted(the_dict.keys())
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
        if file.endswith(".xls") or file.endswith(".xlsx") or file.endswith(".xlsm"):
            self.writer = XLSWriter(file)
        elif file.endswith(".csv"):
            self.writer = CSVWriter(file)
        elif file.endswith(".ods"):
            self.writer = ODSWriter(file)
        else:
            raise NotImplementedError("Cannot open %s" % file)
    
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
                
