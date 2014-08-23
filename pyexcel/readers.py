import csv
from openpyxl import load_workbook
import xlrd


class CSVReader:
    def __init__(self, file):
        self.array = []
        reader = csv.reader(open(file, 'rb'), dialect=csv.excel)
        self.array.extend(reader)

    def first_row(self):
        return 0

    def row_index(self, value):
        return value + 1

    def number_of_rows(self):
        return len(self.array)

    def cell_value(self, row, column):
        return self.array[row][column]

    def row_range(self):
        return range(self.first_row(), self.number_of_rows())


class XLSReader:
    def __init__(self, file):
        self.workbook = xlrd.open_workbook(file)
        self.worksheet = self.workbook.sheet_by_index(0)
        
    def number_of_rows(self):
        return self.worksheet.nrows

    def row_index(self, value):
        return value + 1

    def first_row(self):
        return 0

    def row_range(self):
        return range(self.first_row(), self.number_of_rows())

    def cell_value(self, row, column):
        return self.worksheet.cell_value(row, column)

class XLSXReader:
    def __init__(self, file):
        self.wb = load_workbook(file)
        self.ws = self.wb.active
        self.columns = [x for x in 'ABCDEFGHIJKLMNOPQRST']

    def _get_columns(self, index):
        length = len(self.columns)
        if index < length:
            return self.columns[index]
        else:
            return self._get_columns(index/length) + self.columns[index%length]
            
    def first_row(self):
        return 1

    def row_index(self, value):
        return value

    def number_of_rows(self):
        return self.ws.get_highest_row()

    def row_range(self):
        return range(self.first_row(), self.number_of_rows()+1)

    def cell_value(self, row, column):
        return self.ws.cell("%s%d" % (self._get_columns(column), row)).value

class Reader:
    def __init__(self, file):
        if file.endswith(".xlsx"):
            self.reader = XLSXReader(file)
        elif file.endswith(".xls"):
            self.reader = XLSReader(file)
        elif file.endswith(".csv"):
            self.reader = CSVReader(file)
        else:
            raise NotImplementedError("can not open %s" % file)

    def first_row(self):
        return self.reader.first_row()

    def row_index(self, value):
        return self.reader.row_index(value)

    def number_of_rows(self):
        return self.reader.number_of_rows()

    def cell_value(self, row, column):
        return self.reader.cell_value(row, column)

    def row_range(self):
        return self.reader.row_range()
