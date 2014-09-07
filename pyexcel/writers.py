import csv

class CSVWriter:
    def __init__(self, file):
        self.f = open(file, "wb")
        self.writer = csv.writer(self.f)

    def write_row(self, array):
        self.writer.writerow(array)

    def close(self):
        self.f.close()

class Writer:
    def __init__(self, file):
        if file.endswith(".csv"):
            self.writer = CSVWriter(file)
        else:
            raise NotImplementedError("Cannot open %s" % file)

    def write_row(self, array):
        self.writer.write_row(array)

    def close(self):
        self.writer.close()