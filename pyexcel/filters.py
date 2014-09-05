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
        return len(self.indices)

    def columns(self):
        return 0

    def translate(self, row, column):
        new_row = row
        for i in self.indices:
            if i <= new_row:
                new_row += 1
        return new_row, column


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

        
class FilterReader(Reader):
    def number_of_rows(self):
        """
        Number of rows in the data file
        """
        if self.filter:
            return self.reader.number_of_rows() - self.filter.rows()
        else:
            return self.reader.number_of_rows()
    def number_of_columns(self):
        """
        Number of columns in the data file
        """
        if self.filter:
            return self.reader.number_of_columns() - self.filter.columns()
        else:
            return self.reader.number_of_columns()
    def cell_value(self, row, column):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            if self.filter:
                new_row, new_column = self.filter.translate(row, column)
                return self.reader.cell_value(new_row, new_column)
            else:
                return self.reader.cell_value(row, column)
        else:
            return None
    def filter(self, afilter):
        self.filter = afilter
        self.filter.validate_filter(self)
        return self
