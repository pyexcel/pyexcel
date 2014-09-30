import csv
from pyexcel.datastruct import Cell
from pyexcel.formatters import STRING_FORMAT


class CSVSheet:
    """
    csv sheet
    """
    def __init__(self, sheet):
        self.sheet = sheet
        self.nrows = len(self.sheet)
        self.ncols = self._ncols()

    def number_of_rows(self):
        """
        Number of rows in the csv file
        """
        return self.nrows

    def number_of_columns(self):
        """
        Number of columns in the csv file

        assuming the length of each row is uniform
        """
        return self.ncols

    def _ncols(self):
        if len(self.sheet) > 1:
            # csv reader will get the longest row
            # and use that length
            return len(self.sheet[0])
        else:
            return 0

    def cell_value(self, row, column):
        """
        Random access to the csv cells
        """
        value = self.sheet[row][column]
        cell = Cell(STRING_FORMAT, value)
        return cell


class CSVBook:
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, file):
        self.array = []
        reader = csv.reader(open(file, 'rb'), dialect=csv.excel)
        self.array.extend(reader)

    def sheets(self):
        return {"csv": CSVSheet(self.array)}

