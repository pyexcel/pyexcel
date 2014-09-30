import csv
from pyexcel.datastruct import Cell
from pyexcel.formatters import STRING_FORMAT


class CSVBook:
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, file):
        self.array = []
        reader = csv.reader(open(file, 'rb'), dialect=csv.excel)
        for row in reader:
            myrow = []
            for element in row:
                myrow.append(Cell(STRING_FORMAT, element))
            self.array.append(myrow)

    def sheets(self):
        return {"csv": self.array}

