import csv


class CSVBook:
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, file):
        self.array = []
        reader = csv.reader(open(file, 'rb'), dialect=csv.excel)
        longest_row_length = -1
        for row in reader:
            myrow = []
            for element in row:
                myrow.append(element)
            if longest_row_length == -1:
                longest_row_length = len(myrow)
            elif longest_row_length < len(myrow):
                longest_row_length = len(myrow)
            self.array.append(myrow)
        if len(self.array[0]) < longest_row_length:
            self.array[0] = self.array[0] + [""] * (longest_row_length - len(self.array[0]))
        self.mysheets = {
            "csv": self.array
        }

    def sheets(self):
        return self.mysheets


class CSVSheetWriter:
    """
    csv file writer

    """
    def __init__(self, file, name):
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
