"""
Design assumption:

It is a MxN formed table

"""
import json
from iterators import HorizontalIterator, VerticalIterator, HorizontalReverseIterator, VerticalReverseIterator

class CSVReader:
    """
    csv reader
    """
    def __init__(self, file):
        import csv
        self.array = []
        reader = csv.reader(open(file, 'rb'), dialect=csv.excel)
        self.array.extend(reader)

    def number_of_rows(self):
        """
        Number of rows in the csv file
        """
        return len(self.array)

    def number_of_columns(self):
        """
        Number of columns in the csv file

        assuming the length of each row is uniform
        """
        if len(self.array) > 1:
            return len(self.array[0])
        else:
            return 0

    def cell_value(self, row, column):
        """
        Random access to the csv cells
        """
        return self.array[row][column]

    def json(self):
        """
        Return json representation of the data
        """
        return json.dumps(self.array)

class XLSReader:
    """
    xls reader
    
    Currently only support first sheet in the file
    """
    def __init__(self, file):
        import xlrd
        self.workbook = xlrd.open_workbook(file)
        self.worksheet = self.workbook.sheet_by_index(0)
        
    def number_of_rows(self):
        """
        Number of rows in the xls file
        """
        return self.worksheet.nrows

    def number_of_columns(self):
        """
        Number of columns in the xls file
        """        
        return self.worksheet.ncols

    def cell_value(self, row, column):
        """
        Random access to the xls cells
        """
        return self.worksheet.cell_value(row, column)

    def json(self):
        array = []
        for i in range(0, self.number_of_rows()):
            array.append(self.worksheet.row_values(i,
                                                   start_colx=0,
                                                   end_colx=self.number_of_columns()))
        return json.dumps(array)

        
class ODSReaderImp(CSVReader):
    """
    ods reader

    Currently only support first sheet in the file
    """
    def __init__(self, file):
        import odsreader
        self.ods = odsreader.ODSReader(file)
        keys = self.ods.SHEETS.keys()
        self.array = self.ods.getSheet(keys[0])


class Reader:
    """
    Wrapper class to unify csv, xls and xlsx reader
    """
    def __init__(self, file):
        """
        Reader constructor

        Selecting a specific reader according to file extension
        """
        if file.endswith(".xlsm") or file.endswith(".xlsx") or file.endswith(".xls"):
            self.reader = XLSReader(file)
        elif file.endswith(".csv"):
            self.reader = CSVReader(file)
        elif file.endswith(".ods"):
            self.reader = ODSReaderImp(file)
        else:
            raise NotImplementedError("can not open %s" % file)

    def __iter__(self):
        return HorizontalIterator(self)

    def reverse(self):
        return HorizontalReverseIterator(self)

    def vertical(self):
        return VerticalIterator(self)

    def rvertical(self):
        return VerticalReverseIterator(self)

    def number_of_rows(self):
        """
        Number of rows in the data file
        """
        return self.reader.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data file
        """
        return self.reader.number_of_columns()

    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            return self.reader.cell_value(row, column)
        else:
            return None

    def row_range(self):
        """
        Utility function to get row range
        """
        return range(0, self.reader.number_of_rows())

    def column_range(self):
        """
        Utility function to get column range
        """
        return range(0, self.reader.number_of_columns())

    def json(self):
        return self.reader.json()
