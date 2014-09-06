from readers import Reader
#1 2 3 4 5 6 7
#  x     x
#1   3 4   6 7
#1   2 3   4 5

class ColumnIndexFilter:
    def __init__(self, func):
        self.eval_func = func

    def rows(self):
        return 0

    def columns(self):
        return len(self.indices)

    def validate_filter(self, reader):
        new_indices = []
        for i in reader.column_range():
            if self.eval_func(i):
                new_indices.append(i)
        self.indices = new_indices

    def translate(self, row, column):
        new_column = column
        for i in self.indices:
            if i <= new_column:
                new_column += 1
        return row, new_column


class ColumnFilter(ColumnIndexFilter):
    def __init__(self, indices):
        eval_func = lambda x: x in indices
        ColumnIndexFilter.__init__(self, eval_func)


class OddColumnFilter(ColumnIndexFilter):
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 1
        ColumnIndexFilter.__init__(self, eval_func)


class EvenColumnFilter(ColumnIndexFilter):
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 0
        ColumnIndexFilter.__init__(self, eval_func)


class RowIndexFilter:
    def __init__(self, func):
        self.eval_func = func
        self.indices = None

    def validate_filter(self, reader):
        new_indices = []
        for i in reader.row_range():
            if self.eval_func(i):
                new_indices.append(i)
        self.indices = new_indices

    def rows(self):
        if self.indices:
            return len(self.indices)
        else:
            return 0

    def columns(self):
        return 0

    def translate(self, row, column):
        if self.indices:
            new_row = row
            for i in self.indices:
                if i <= new_row:
                    new_row += 1
            return new_row, column
        else:
            return row, column


class RowFilter(RowIndexFilter):
    def __init__(self, indices):
        eval_func = lambda x: x in indices
        RowIndexFilter.__init__(self, eval_func)


class OddRowFilter(RowIndexFilter):
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 1
        RowIndexFilter.__init__(self, eval_func)


class EvenRowFilter(RowIndexFilter):
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 0
        RowIndexFilter.__init__(self, eval_func)


class RowValueFilter(RowIndexFilter):

    def validate_filter(self, reader):
        new_indices = []
        index = 0
        for r in reader.rows():
            if not self.eval_func(r):
                new_indices.append(index)
            index += 1
        self.indices = new_indices

class RowInFileFilter(RowValueFilter):

    def __init__(self, reader):
        filter_func = lambda row_a: reader.contains((lambda row_b: row_a == row_b))
        RowValueFilter.__init__(self, filter_func)

        
class FilterReader(Reader):
    _filter = None
    def row_range(self):
        if self._filter:
            new_rows = self.reader.number_of_rows() - self._filter.rows()
            return range(0, new_rows)
        else:
            return range(0, self.reader.number_of_rows())
        
    def column_range(self):
        if self._filter:
            new_columns = self.reader.number_of_columns() - self._filter.columns()
            return range(0, new_columns)
        else:
            return range(0, self.reader.number_of_columns())
        
    def number_of_rows(self):
        """
        Number of rows in the data file
        """
        if self._filter:
            return self.reader.number_of_rows() - self._filter.rows()
        else:
            return self.reader.number_of_rows()
    def number_of_columns(self):
        """
        Number of columns in the data file
        """
        if self._filter:
            return self.reader.number_of_columns() - self._filter.columns()
        else:
            return self.reader.number_of_columns()
    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            if self._filter:
                new_row, new_column = self._filter.translate(row, column)
                return self.reader.cell_value(new_row, new_column)
            else:
                return self.reader.cell_value(row, column)
        else:
            return None
    def filter(self, afilter):
        afilter.validate_filter(self)
        self._filter = afilter
        return self
