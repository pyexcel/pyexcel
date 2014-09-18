"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for reading different excel file formats

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from iterators import (HBRTLIterator,
                       HTLBRIterator,
                       VBRTLIterator,
                       VTLBRIterator,
                       RowIterator,
                       RowReverseIterator,
                       ColumnIterator,
                       ColumnReverseIterator,
                       SeriesColumnIterator,
                       SheetIterator)
from filters import (RowIndexFilter,
                     ColumnIndexFilter,
                     RowFilter)

class CSVSheet:
    """
    csv sheet
    """
    def __init__(self, sheet):
        self.array = sheet

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
        value = self.array[row][column]
        try:
            if "." in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return value


class CSVBook:
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, file):
        import csv
        self.array = []
        reader = csv.reader(open(file, 'rb'), dialect=csv.excel)
        self.array.extend(reader)

    def number_of_sheets(self):
        """
        Number of sheets in the csv file
        """
        return 1

    def sheet_names(self):
        """Get a list of sheet names"""        
        return ["csv"]

    def sheets(self):
        return {"csv": CSVSheet(self.array)}


class XLSSheet:
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
        return self.worksheet.cell_value(row, column)


class XLSBook:
    """
    XLSBook reader

    It reads xls, xlsm, xlsx work book
    """

    def __init__(self, file):
        import xlrd
        self.workbook = xlrd.open_workbook(file)

    def number_of_sheets(self):
        """
        Number of sheets in the csv file
        """
        return self.workbook.nsheets

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.workbook.sheet_names()

    def sheets(self):
        ret = {}
        for name in self.workbook.sheet_names():
            ret[name] = XLSSheet(self.workbook.sheet_by_name(name))
        return ret


class ODSBook:
    """
    ODS Book reader

    It reads ods file
    """

    def __init__(self, file):
        import ext.odsreader as odsreader
        self.ods = odsreader.ODSReader(file)

    def number_of_sheets(self):
        """
        Number of sheets in the ods file
        """
        return len(self.ods.SHEETS.keys())

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.ods.sheetNames()

    def sheets(self):
        ret = {}
        for name in self.ods.SHEETS.keys():
            ret[name] = CSVSheet(self.ods.SHEETS[name])
        return ret


class PlainSheet:
    """
    Wrapper class to unify csv, xls and xlsx sheet
    """
    def __init__(self, sheet):
        """
        Sheet constructor

        Selecting a specific sheet according to file extension
        """
        self.sheet = sheet

    def __iter__(self):
        """
        Default iterator to go through each cell one by one from top row to
        bottom row and from left to right
        """
        return self.rows()
        
    def enumerate(self):
        """
        Default iterator to go through each cell one by one from top row to
        bottom row and from left to right
        """
        return HTLBRIterator(self)

    def reverse(self):
        """
        Reverse iterator to go through each cell one by one from
        bottom row to top row and from right to left
        """
        return HBRTLIterator(self)

    def vertical(self):
        """
        Default iterator to go through each cell one by one from
        leftmost column to rightmost row and from top to bottom
        """
        return VTLBRIterator(self)

    def rvertical(self):
        """
        Default iterator to go through each cell one by one from rightmost
        column to leftmost row and from bottom to top
        """
        return VBRTLIterator(self)

    def rows(self):
        """
        Returns a row iterator to go through each row from top to bottom
        """
        return RowIterator(self)

    def rrows(self):
        """
        Returns a row iterator to go through each row from bottom to top
        """
        return RowReverseIterator(self)

    def columns(self):
        """
        Returns a column iterator to go through each column from left to right
        """
        return ColumnIterator(self)

    def rcolumns(self):
        """
        Returns a column iterator to go through each column from right to left
        """
        return ColumnReverseIterator(self)

    def number_of_rows(self):
        """
        Number of rows in the data sheet
        """
        return self.sheet.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data sheet
        """
        return self.sheet.number_of_columns()

    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            return self.sheet.cell_value(row, column)
        else:
            return None

    def row_range(self):
        """
        Utility function to get row range
        """
        return range(0, self.sheet.number_of_rows())

    def column_range(self):
        """
        Utility function to get column range
        """
        return range(0, self.sheet.number_of_columns())

    def row_at(self, index):
        """
        Returns an array that collects all data at the specified row
        """
        if index in self.row_range():
            cell_array = []
            for i in self.column_range():
                cell_array.append(self.cell_value(index, i))
            return cell_array
        else:
            return None

    def column_at(self, index):
        """
        Returns an array that collects all data at the specified column
        """
        if index in self.column_range():
            cell_array = []
            for i in self.row_range():
                cell_array.append(self.cell_value(i, index))
            return cell_array
        else:
            return None

    def contains(self, predicate):
        for r in self.rows():
            if predicate(r):
                return True
        else:
            return False


class MultipleFilterableSheet(PlainSheet):
    """
    Sheet that can be applied one filter
    """
    def __init__(self, sheet):
        PlainSheet.__init__(self, sheet)
        self._filters = []

    def row_range(self):
        """
        row range
        """
        return range(0, self.number_of_rows())

    def column_range(self):
        """
        column range
        """
        return range(0, self.number_of_columns())

    def number_of_rows(self):
        """
        Number of rows in the data sheet
        """
        if len(self._filters) != 0:
            new_rows = self.sheet.number_of_rows()
            for filter in self._filters:
                new_rows = new_rows - filter.rows()
            return new_rows
        else:
            return self.sheet.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data sheet
        """
        if len(self._filters) != 0:
            new_cols = self.sheet.number_of_columns()
            for filter in self._filters:
                new_cols = new_cols - filter.columns()
            return new_cols
        else:
            return self.sheet.number_of_columns()

    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            if len(self._filters) != 0:
                new_row = row
                new_column = column
                number_of_filters = len(self._filters)
                for i in range(number_of_filters-1, -1, -1):
                    new_row, new_column = self._filters[i].translate(new_row, new_column)
                return self.sheet.cell_value(new_row, new_column)
            else:
                return self.sheet.cell_value(row, column)
        else:
            return None

    def add_filter(self, afilter):
        afilter.validate_filter(self)
        self._filters.append(afilter)
        return self

    def remove_filter(self, afilter):
        self._filters.remove(afilter)
        for fitler in self._filters:
            filter.validate_filter(self)

    def clear_filters(self):
        self._filters = []


class FilterableSheet(MultipleFilterableSheet):
    """
    Sheet that can be applied one filter
    """
    
    def filter(self, afilter):
        self.add_filter(afilter)


class Sheet(MultipleFilterableSheet):
    def __init__(self, sheet, name):
        MultipleFilterableSheet.__init__(self, sheet)
        self.column_filters = []
        self.row_filters = []
        self.headers = None
        self.signature_filter = None
        self.name = name
        
    def become_series(self):
        """
        Evolve this sheet to a SeriesReader
        """
        self.signature_filter = RowFilter([0])
        self._validate_filters()

    def become_sheet(self):
        """
        Evolve back to plain sheet reader
        """
        self.signature_filter = None
        self._validate_filters()

    def add_filter(self, afilter):
        """
        Add a custom filter
        """
        if isinstance(afilter, ColumnIndexFilter):
            self.column_filters.append(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self.row_filters.append(afilter)
        self._validate_filters()

    def clear_filters(self):
        """
        Clear all filters
        """
        self.column_filters = []
        self.row_filters = []
        self._validate_filters()

    def remove_filter(self, afilter):
        """
        Remove a named custom filter
        """
        if isinstance(afilter, ColumnIndexFilter):
            self.column_filters.remove(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self.row_filters.remove(afilter)
        self._validate_filters()

    def _validate_filters(self):
        if self.signature_filter:
            local_filters = self.column_filters + [self.signature_filter] + self.row_filters
        else:
            local_filters = self.column_filters + self.row_filters
        self._filters = []
        for filter in local_filters:
            filter.validate_filter(self)
            self._filters.append(filter)

    def _headers(self):
        self.headers = []
        for i in self.column_range():
            new_row = 0
            new_column = i
            number_of_column_filters = len(self.column_filters)
            for x in range(number_of_column_filters-1, -1, -1):
                new_row, new_column = self.column_filters[x].translate(new_row, new_column)
            self.headers.append(self.sheet.cell_value(0, new_column))

    def series(self):
        """
        Return column headers
        """
        if self.signature_filter:
            self._headers()
            return self.headers
        else:
            return []

    def named_column_at(self, name):
        """Get a column by its name """
        if self.signature_filter:
            self._headers()
            index = self.headers.index(name)
            column_array = self.column_at(index)
            return {name: column_array}
        else:
            return {}

    def __iter__(self):
        if self.signature_filter:
            return SeriesColumnIterator(self)
        else:
            return MultipleFilterableSheet.__iter__(self)

class BookReader:
    def __init__(self, file):
        """
        Book constructor

        Selecting a specific book according to file extension
        """
        if (file.endswith(".xlsm") or file.endswith(".xlsx") or file.endswith(".xls")):
            self.book = XLSBook(file)
        elif file.endswith(".csv"):
            self.book = CSVBook(file)
        elif file.endswith(".ods"):
            self.book = ODSBook(file)
        else:
            raise NotImplementedError("can not open %s" % file)
        self.current_sheet = 0
        self.sheet_array = []
        self.sheet_dict = {}
        self.sheets = self.book.sheets()
        for name in self.sheets.keys():
            sheet = Sheet(self.sheets[name], name)
            self.sheet_array.append(sheet)
            self.sheet_dict[name] = sheet

    def __iter__(self):
        return SheetIterator(self)

    def number_of_sheets(self):
        return len(self.sheet_array)

    def sheet_names(self):
        return self.sheet_dict.keys()

    def sheet_by_name(self, name):
        return self.sheet_dict[name]

    def sheet_by_index(self, index):
        if index < len(self.sheet_array):
            return self.sheet_array[index]

    def __getitem__(self, key):
        if type(key) == int:
            return self.sheet_by_index(key)
        else:
            return self.sheet_by_name(key)
        
class FilterableReader(FilterableSheet):
    """
    Sheet that can be applied one filter
    """
    def __init__(self, file):
        self.book = BookReader(file)
        FilterableSheet.__init__(self, self.book[0].sheet)

class Reader(Sheet):
    """
    A single sheet excel file reader
    """
    
    def __init__(self, file):
        self.book = BookReader(file)
        Sheet.__init__(self, self.book[0].sheet, self.book[0].name)


class SeriesReader(Reader):
    """
    A single sheet excel file reader and it has column headers
    """
    
    def __init__(self, file):
        Reader.__init__(self, file)
        self.become_series()

