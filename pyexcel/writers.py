class ODSWriter:
    """
    Write MxN '*.ods' files
    """
    def __init__(self, file):
        from odf.opendocument import OpenDocumentSpreadsheet
        from odf.table import Table
        self.doc = OpenDocumentSpreadsheet()
        self.table = Table(name="pyexcel_data")
        self.file = file

    def write_row(self, array):
        from odf.table import TableRow, TableCell
        from odf.text import P
        tr = TableRow()
        self.table.addElement(tr)
        for x in array:
            tc = TableCell()
            tc.addElement(P(text=x))
            tr.addElement(tc)

    def close(self):
        self.doc.spreadsheet.addElement(self.table)
        self.doc.write(self.file)


class CSVWriter:
    def __init__(self, file):
        import csv
        self.f = open(file, "wb")
        self.writer = csv.writer(self.f)

    def write_row(self, array):
        self.writer.writerow(array)

    def close(self):
        self.f.close()

        
class XLSWriter:
    def __init__(self, file):
        import xlwt
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
            self.writer = XLSWriter(file)
        elif file.endswith(".ods"):
            self.writer = ODSWriter(file)
        else:
            raise NotImplementedError("Cannot open %s" % file)

    def write_row(self, array):
        self.writer.write_row(array)

    def write_table(self, table):
        """
        Write a table

        table can be two dimensional array or a row iterator
        """
        for row in table:
            self.writer.write_row(row)

    def write_reader(self, reader):
        self.write_table(reader.rows())

    def write_hat_table(self, the_dict):
        keys = the_dict.keys()
        self.writer.write_row(keys)
        min_length = -1
        for k in keys:
            column_length = len(the_dict[k])
            if min_length == -1:
                min_length = column_length
            elif min_length > column_length:
                min_length = column_length
        for i in range(0, min_length):
            row_data = []
            for k in keys:
                row_data.append(the_dict[k][i])
            self.writer.write_row(row_data)
            
    def close(self):
        self.writer.close()