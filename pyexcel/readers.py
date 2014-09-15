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
                       SeriesColumnIterator)
from filters import (RowIndexFilter,
                     ColumnIndexFilter,
                     RowFilter)


class CSVReader:
    """
    csv reader
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
        return 0

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        pass

    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        pass

    def sheet_names(self):
        """Get a list of sheet names"""        
        return ["csv"]

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


class XLSReader:
    """
    xls reader

    Currently only support first sheet in the file
    """
    def __init__(self, file):
        import xlrd
        self.workbook = xlrd.open_workbook(file)
        self.worksheet = self.workbook.sheet_by_index(0)

    def number_of_sheets(self):
        """
        Number of sheets in the csv file
        """
        return self.workbook.nsheets

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        if index < self.workbook.nsheets:
            self.worksheet = self.workbook.sheet_by_index(0)

    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        self.worksheet = self.workbook.sheet_by_name(name)

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.workbook.sheet_names()

    def number_of_rows(self):
        """
        Number of rows in the xls file
        """
        return self.worksheet.nrows

    def number_of_columns(self):
        """
        Number of columns in the xls file
        """
        return self.worksheet.ncols

    def cell_value(self, row, column):
        """
        Random access to the xls cells
        """
        return self.worksheet.cell_value(row, column)


class ODSReaderImp(CSVReader):
    """
    ods reader

    Currently only support first sheet in the file
    """
    def __init__(self, file):
        import ext.odsreader as odsreader
        self.ods = odsreader.ODSReader(file)
        self.use_sheet_at_index(0)

    def number_of_sheets(self):
        """
        Number of sheets in the ods file
        """
        return len(self.ods.SHEETS.keys())

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        self.array = self.ods.getSheetByIndex(index)

    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        self.array =  self.ods.getSheet(name)

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.ods.sheetNames()


class PlainReader:
    """
    Wrapper class to unify csv, xls and xlsx reader
    """
    def __init__(self, file):
        """
        Reader constructor

        Selecting a specific reader according to file extension
        """
        if (file.endswith(".xlsm") or file.endswith(".xlsx") or file.endswith(".xls")):
            self.reader = XLSReader(file)
        elif file.endswith(".csv"):
            self.reader = CSVReader(file)
        elif file.endswith(".ods"):
            self.reader = ODSReaderImp(file)
        else:
            raise NotImplementedError("can not open %s" % file)
        self.current_sheet = 0

    def __iter__(self):
        """
        Default iterator to go through each cell one by one from top row to
        bottom row and from left to right
        """
        return self.enumerate()
        
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
        Number of rows in the data file
        """
        return self.reader.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data file
        """
        return self.reader.number_of_columns()

    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            return self.reader.cell_value(row, column)
        else:
            return None

    def row_range(self):
        """
        Utility function to get row range
        """
        return range(0, self.reader.number_of_rows())

    def column_range(self):
        """
        Utility function to get column range
        """
        return range(0, self.reader.number_of_columns())

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

    def number_of_sheets(self):
        """
        Number of sheets in the ods file
        """
        return self.reader.number_of_sheets()

    def use_sheet_at_index(self, index):
        """Switch sheet for reading"""
        self.reader.use_sheet_at_index(index)
        self.current_sheet = index
        
    def use_sheet_named_as(self, name):
        """Switch sheet for reading"""        
        self.reader.use_sheet_named_as(name)
        names = self.sheet_names()
        index = names.index(name)
        self.current_sheet = index

    def sheet_names(self):
        """Get a list of sheet names"""        
        return self.reader.sheet_names()

    def sheet(self):
        """Get current sheet index"""
        return self.current_sheet

class MultipleFilterableReader(PlainReader):
    """
    Reader that can be applied one filter
    """
    def __init__(self, file):
        PlainReader.__init__(self, file)
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
        Number of rows in the data file
        """
        if len(self._filters) != 0:
            new_rows = self.reader.number_of_rows()
            for filter in self._filters:
                new_rows = new_rows - filter.rows()
            return new_rows
        else:
            return self.reader.number_of_rows()

    def number_of_columns(self):
        """
        Number of columns in the data file
        """
        if len(self._filters) != 0:
            new_cols = self.reader.number_of_columns()
            for filter in self._filters:
                new_cols = new_cols - filter.columns()
            return new_cols
        else:
            return self.reader.number_of_columns()

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
                return self.reader.cell_value(new_row, new_column)
            else:
                return self.reader.cell_value(row, column)
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


class FilterableReader(MultipleFilterableReader):
    """
    Reader that can be applied one filter
    """
    
    def filter(self, afilter):
        self.add_filter(afilter)


class Reader(MultipleFilterableReader):
    def __init__(self, file):
        MultipleFilterableReader.__init__(self, file)
        self.column_filters = []
        self.row_filters = []
        self.headers = None
        self.signature_filter = None
        
    def become_series(self):
        self.signature_filter = RowFilter([0])
        self._validate_filters()

    def add_filter(self, afilter):
        if isinstance(afilter, ColumnIndexFilter):
            self.column_filters.append(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self.row_filters.append(afilter)
        self._validate_filters()

    def remove_column_filter(self, afilter):
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
            self.headers.append(self.reader.cell_value(0, new_column))

    def series(self):
        if self.signature_filter:
            self._headers()
            return self.headers
        else:
            return []

    def named_column_at(self, name):
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
            return MultipleFilterableReader.__iter__(self)


class SeriesReader(Reader):
    def __init__(self, file):
        Reader.__init__(self, file)
        self.become_series()
    

#class GenericSeriesReader(FilterableReader):
#    """
#    For data with column headers
#
#    x y z
#    1 2 3
#    4 5 6
#
#    This class has a default filter that filter out
#    row 0 as headers. Extra functions were added
#    to return headers at row 0
#    """
#    def __init__(self, reader):
#        self.reader = reader
#        # filter out the first row
#        self.filter(RowFilter([0]))
#        self.headers = None
#
#    def _headers(self):
#        self.headers = []
#        for i in self.column_range():
#            self.headers.append(self.reader.cell_value(0, i))
#
#    def series(self):
#        self._headers()
#        return self.headers
#
#    def named_column_at(self, name):
#        self._headers()
#        index = self.headers.index(name)
#        column_array = self.column_at(index)
#        return {name: column_array}
#
#    def __iter__(self):
#        return SeriesColumnIterator(self)
#
#
#class StaticSeriesReader(GenericSeriesReader):
#    """
#
#    Static Series Reader. No filters can be applied.
#    """
#    def __init__(self, file):
#        reader = Reader(file)
#        GenericSeriesReader.__init__(self, reader)
#
#
#class ColumnFilterableSeriesReader(GenericSeriesReader):
#    """
#
#    Columns can be filtered but not rows
#    """
#    def __init__(self, file):
#        self.reader = FilterableReader(file)
#        GenericSeriesReader.filter(self, RowFilter([0]))
#        self.headers = None
#
#    def filter(self, filter):
#        self.reader.filter(filter)
#        self._filter.validate_filter(self)
#
#
#class SeriesReader(GenericSeriesReader):
#    """
#
#    rows other than header row can be filtered. row number
#    has been shifted by 1 as header row is protected.
#
#    columns can be filtered.
#    """
#    def __init__(self, file):
#        self.reader = ColumnFilterableSeriesReader(file)
#
#    def series(self):
#        return self.reader.series()
#
#    def named_column_at(self, name):
#        headers = self.series()
#        index = headers.index(name)
#        column_array = self.column_at(index)
#        return {name: column_array}
#
#    def filter(self, afilter):
#        if isinstance(afilter, ColumnIndexFilter):
#            self.reader.filter(afilter)
#        else:
#            GenericSeriesReader.filter(self, afilter)
