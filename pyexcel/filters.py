"""
    pyexcel.filters
    ~~~~~~~~~~~~~~~

    Filtering functions for pyexcel readers

    :copyright: (c) 2014 by C. W.
    :license: GPL v3

    Design note for filter algorithm::
    
        #1 2 3 4 5 6 7  <- original index
        #  x     x
        #1   3 4   6 7  <- filtered index
        #1   2 3   4 5  <- actual index after filtering
    
    Design note for multiple filter algorithm::
    
        #    1 2 3 4 5 6 7 8 9
        f1     x       x
             1   2 3 4   5 6 7
        f2       x   x     x
             1     2     3   4
        f3         x
             1           2   3
"""
class IndexFilter:
    """A generic index filter"""
    def __init__(self, func):
        """Constructor
        :param Function func: a evaluation function
        """
        self.eval_func = func
        # indices to be filtered out
        self.indices = None

    def rows(self):
        """Rows that were filtered out
        """
        return 0
    def columns(self):
        """Columns that were filtered out"""
        return 0

    def validate_filter(self, reader):
        """
        Find out which column index to be filtered

        :param Matrix reader: a Matrix instance
        
        """
        pass

    def translate(self, row, column):
        """Map the row, column after filtering to the
        original ones before filtering"""
        pass


class ColumnIndexFilter(IndexFilter):
    """A column filter that operates on column indices"""
    def columns(self):
        """Columns that were filtered out"""
        return len(self.indices)

    def validate_filter(self, reader):
        """
        Find out which column index to be filtered

        :param Matrix reader: a Matrix instance
        """
        self.indices = [ i for i in reader.column_range() if self.eval_func(i) ]

    def translate(self, row, column):
        """Map the row, column after filtering to the
        original ones before filtering

        :param int row: row index after filtering
        :param int column: column index after filtering
        :returns: set of (row, new_column) 
        """
        if self.indices:
            new_column = column
            for i in self.indices:
                if i <= new_column:
                    new_column += 1
            return row, new_column
        else:
            return row, column


class ColumnFilter(ColumnIndexFilter):
    """A column filter that takes in a list of indices to be
    filtered out""" 
    def __init__(self, indices):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        eval_func = lambda x: x in indices
        ColumnIndexFilter.__init__(self, eval_func)


class SingleColumnFilter(ColumnIndexFilter):
    """A column filter that takes in a list of indices to be
    filtered out""" 
    def __init__(self, index):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        eval_func = lambda x: x == index
        ColumnIndexFilter.__init__(self, eval_func)


class OddColumnFilter(ColumnIndexFilter):
    """A column filter that filters out odd indices

    * column 0 is regarded as the first column.
    * column 1 is regarded as the seocond column -> this will be filtered out
    """
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 1
        ColumnIndexFilter.__init__(self, eval_func)


class EvenColumnFilter(ColumnIndexFilter):
    """A column filter that filters out even indices

    * column 0 is regarded as the first column. -> this will be filtered out
    * column 1 is regarded as the seocond column
    """
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 0
        ColumnIndexFilter.__init__(self, eval_func)


class RowIndexFilter(IndexFilter):
    """A row filter that operates on column indices"""
    def rows(self):
        """number of rows to be filtered out"""
        if self.indices:
            return len(self.indices)
        else:
            return 0

    def validate_filter(self, reader):
        """
        Find out which column index to be filtered

        :param Matrix reader: a Matrix instance
        """
        self.indices = [ i for i in reader.row_range() if self.eval_func(i) ]

    def translate(self, row, column):
        """Map the row, column after filtering to the
        original ones before filtering

        :param int row: row index after filtering
        :param int column: column index after filtering
        :returns: set of (row, new_column) 
        """
        if self.indices:
            new_row = row
            for i in self.indices:
                if i <= new_row:
                    new_row += 1
            return new_row, column
        else:
            return row, column


class RowFilter(RowIndexFilter):
    """A row filter that takes in a list of indices to be
    filtered out""" 
    def __init__(self, indices):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        eval_func = lambda x: x in indices
        RowIndexFilter.__init__(self, eval_func)


class SingleRowFilter(RowIndexFilter):
    """A row filter that takes in a list of indices to be
    filtered out""" 
    def __init__(self, index):
        """Constructor

        :param list indices: a list of column indices to be filtered out
        """
        eval_func = lambda x: x == index
        RowIndexFilter.__init__(self, eval_func)


class OddRowFilter(RowIndexFilter):
    """
    Filter out odd rows

    row 0 is seen as the first row
    """
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 1
        RowIndexFilter.__init__(self, eval_func)


class EvenRowFilter(RowIndexFilter):
    """
    Filter out even rows

    row 0 is seen as the first row
    """
    def __init__(self):
        eval_func = lambda x: (x+1) % 2 == 0
        RowIndexFilter.__init__(self, eval_func)


class RowValueFilter(RowIndexFilter):
    """Filter out rows that satisfy a condition

    .. note:: it takes time as it needs to go through all values
    """
    def validate_filter(self, reader):
        """
        Filter out the row indices

        This is what it does::
        
            new_indices = []
            index = 0
            for r in reader.rows():
                if not self.eval_func(r):
                    new_indices.append(index)
                index += 1
        
        :param Matrix reader: a Matrix instance
        """
        self.indices = [row[0] for row in enumerate(reader.rows()) if not self.eval_func(row[1])]


class SeriesRowValueFilter(RowIndexFilter):
    """Filter out rows that satisfy a condition

    .. note:: it takes time as it needs to go through all values
    """
    def validate_filter(self, reader):
        """
        Filter out the row indices

        This is what it does::
        
            new_indices = []
            index = 0
            for r in reader.rows():
                if not self.eval_func(r):
                    new_indices.append(index)
                index += 1
        
        :param Matrix reader: a Matrix instance
        """
        series = reader.row_series
        self.indices = [row[0] for row in enumerate(reader.rows()) if not self.eval_func(dict(zip(series, row[1])))]


class RowInFileFilter(RowValueFilter):
    """Filter out rows that has a row from another reader"""
    def __init__(self, reader):
        """
        Constructor

        :param Matrix reader: a Matrix instance
        """
        func = lambda row_a: reader.contains((lambda row_b: row_a == row_b))
        RowValueFilter.__init__(self, func)
