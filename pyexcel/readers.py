import csv
from openpyxl import load_workbook
import xlrd

def none_value(value):
    if value is None:
        return ""
    else:
        if isinstance(value, unicode):
            str_value = value.encode('ascii', 'xmlcharrefreplace')
        else:
            str_value = str(value)
        str_value.replace('"', '')
        return str_value

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
        return none_value(self.array[row][column].strip().rstrip())

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

    def cell_value(self, row, column):
        return none_value(self.worksheet.cell_value(row, column).strip().rstrip())

class XLSXReader:
    def __init__(self, file):
        self.wb = load_workbook(file)
        self.ws = self.wb.active
        self.columns = [x for x in 'ABCDEFGHIJKLMNOPQRST']

    def _get_columns(self, index):
        len = len(self.columns)
        if index < len:
            return self.columns[index]
        else:
            return self._get_columns(index/len) + self.columns[index%len]
            
    def first_row(self):
        return 1

    def row_index(self, value):
        return value

    def number_of_rows(self):
        return self.ws.get_highest_row() + 1

    def cell_value(self, row, column):
        return none_value(self.ws.cell("%s%d" % (self._get_columns(column), row)).value).strip()

class ReaderFactory:

    @staticmethod
    def get_reader(file):
        if file.endswith(".xlsx"):
            reader = XLSXReader(file)
        elif file.endswith(".xls"):
            reader = XLSReader(file)
        elif file.endswith(".csv"):
            reader = CSVReader(file)
        else:
            reader = None
        return reader
