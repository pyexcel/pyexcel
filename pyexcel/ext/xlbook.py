from pyexcel.common import XLS_FORMAT_CONVERSION, DATE_FORMAT, RawSheet, Sheet
import datetime
import xlrd
import xlwt


def xldate_to_python_date(value):
    date_tuple = xlrd.xldate_as_tuple(value, 0)
    ret = None
    if date_tuple == (0, 0, 0, 0, 0, 0):
        ret = datetime.datetime(1900, 1, 1, 0, 0, 0)
    elif date_tuple[0:3] == (0, 0, 0):
        ret = datetime.time(date_tuple[3],
                            date_tuple[4],
                            date_tuple[5])
    elif date_tuple[3:6] == (0, 0, 0):
        ret = datetime.date(date_tuple[0],
                            date_tuple[1],
                            date_tuple[2])
    return ret


class XLSheet:
    """
    xls sheet

    Currently only support first sheet in the file
    """
    def __init__(self, sheet):
        self.worksheet = sheet

    def number_of_rows(self):
        """
        Number of rows in the xls sheet
        """
        return self.worksheet.nrows

    def number_of_columns(self):
        """
        Number of columns in the xls sheet
        """
        return self.worksheet.ncols

    def cell_value(self, row, column):
        """
        Random access to the xls cells
        """
        cell_type = self.worksheet.cell_type(row, column)
        my_type = XLS_FORMAT_CONVERSION[cell_type]
        value = self.worksheet.cell_value(row, column)
        if my_type == DATE_FORMAT:
            value = xldate_to_python_date(value)
        return value


def to_array(sheet):
    array = []
    for r in range(0, sheet.number_of_rows()):
        row = []
        for c in range(0, sheet.number_of_columns()):
            row.append(sheet.cell_value(r, c))
        array.append(row)
    return array


class XLBook:
    """
    XLSBook reader

    It reads xls, xlsm, xlsx work book
    """

    def __init__(self, file):
        self.workbook = xlrd.open_workbook(file)
        self.mysheets = {}
        for name in self.workbook.sheet_names():
            data = to_array(XLSheet(
                self.workbook.sheet_by_name(name)))
            self.mysheets[name] = Sheet(RawSheet(data), name)

    def sheets(self):
        """Get sheets in a dictionary"""
        return self.mysheets


class XLSheetWriter:
    """
    xls, xlsx and xlsm sheet writer
    """
    def __init__(self, wb, name):
        self.wb = wb
        if name:
            sheet_name = name
        else:
            sheet_name = "pyexcel_sheet1"
        self.ws = self.wb.add_sheet(sheet_name)
        self.current_row = 0

    def write_row(self, array):
        """
        write a row into the file
        """
        for i in range(0, len(array)):
            value = array[i]
            style = None
            tmp_array = []
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                tmp_array = [value.year, value.month, value.day]
                value = xlrd.xldate.xldate_from_date_tuple(tmp_array, 0)
                style = xlwt.XFStyle()
                style.num_format_str = "DD/MM/YY"
            elif isinstance(value, datetime.time):
                tmp_array = [value.hour, value.minute, value.second]
                value = xlrd.xldate.xldate_from_time_tuple(tmp_array)
                style = xlwt.XFStyle()
                style.num_format_str = "HH:MM:SS"
            if style:
                self.ws.write(self.current_row, i, value, style)
            else:
                self.ws.write(self.current_row, i, value)
        self.current_row += 1

    def close(self):
        """
        This call actually save the file
        """
        pass


class XLWriter:
    """
    xls, xlsx and xlsm writer
    """
    def __init__(self, file):
        self.file = file
        self.wb = xlwt.Workbook()
        self.current_row = 0

    def create_sheet(self, name):
        return XLSheetWriter(self.wb, name)

    def close(self):
        """
        This call actually save the file
        """
        self.wb.save(self.file)
