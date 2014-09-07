import sys
print sys.path
import xlwt

class CSVWriter:
    def __init__(self, file):
        import csv
        self.f = open(file, "wb")
        self.writer = csv.writer(self.f)

    def write_row(self, array):
        self.writer.writerow(array)

    def close(self):
        self.f.close()

class XlsWriter:
    def __init__(self, file):
        self.file = file
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet("pyexcel_data")
        self.current_row = 0

    def write_row(self, array):
        for i in range(0, len(array)):
            self.ws.write(self.current_row, i, array[i])
        self.current_row += 1
        if self.ws.col(0).width < len(array):
            self.ws.col(0).width = len(array)

    def close(self):
        self.wb.save(self.file)

class Writer:
    def __init__(self, file):
        if file.endswith(".csv"):
            self.writer = CSVWriter(file)
        elif file.endswith(".xls") or file.endswith(".xlsx") or file.endswith(".xlsm"):
            self.writer = XlsWriter(file)
        else:
            raise NotImplementedError("Cannot open %s" % file)

    def write_row(self, array):
        self.writer.write_row(array)

    def close(self):
        self.writer.close()