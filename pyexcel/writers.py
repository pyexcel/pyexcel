"""
    pyexcel.writers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for writing different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from utils import to_dict
from readers import SeriesReader


class ODSWriter:
    """
    open document spreadsheet writer
    
    """
    def __init__(self, file):
        from odf.opendocument import OpenDocumentSpreadsheet
        from odf.table import Table
        self.doc = OpenDocumentSpreadsheet()
        self.table = Table(name="pyexcel_data")
        self.file = file

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
        self.doc.write(self.file)


class CSVWriter:
    """
    csv file writer
    
    """
    def __init__(self, file):
        import csv
        self.f = open(file, "wb")
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


class XLSWriter:
    """
    xls, xlsx and xlsm writer
    """
    def __init__(self, file):
        import xlwt
        self.file = file
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet("pyexcel_data")
        self.current_row = 0

    def write_row(self, array):
        """
        write a row into the file
        """
        for i in range(0, len(array)):
            self.ws.write(self.current_row, i, array[i])
        self.current_row += 1
        if self.ws.col(0).width < len(array):
            self.ws.col(0).width = len(array)

    def close(self):
        """
        This call actually save the file
        """
        self.wb.save(self.file)


class Writer:
    """
    Uniform excel writer

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
