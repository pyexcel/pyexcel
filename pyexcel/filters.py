from readers import Reader
#1 2 3 4 5 6 7
#  x     x
#1   3 4   6 7
#1   2 3   4 5

class ColumnFilter:
    def __init__(self, indices):
        self.indices = sorted(indices)

    def rows(self):
        return 0

    def columns(self):
        return len(self.indices)

    def validate_filter(self, reader):
        new_indices = []
        for i in self.indices:
            if i in reader.column_range():
                new_indices.append(i)
        self.indices = new_indices

    def translate(self, row, column):
        new_column = column
        for i in self.indices:
            if i <= new_column:
                new_column += 1
        return row, new_column

class RowFilter:
    def __init__(self, indices):
        self.indices = sorted(indices)

    def rows(self):
        return len(self.indices)

    def columns(self):
        return 0

    def validate_filter(self, reader):
        new_indices = []
        for i in self.indices:
            if i in reader.row_range():
                new_indices.append(i)
        self.indices = new_indices

    def translate(self, row, column):
        new_row = row
        for i in self.indices:
            if i <= new_row:
                new_row += 1
        return new_row, column


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
