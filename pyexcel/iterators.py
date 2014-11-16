"""
    pyexcel.iterators
    ~~~~~~~~~~~~~~~~~~~

    Iterate through the two dimensional arrays

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""


class PyexcelIterator:
    """
    A parent class is used to distiguish pyexcel iterators in pyexcel utilities
    """
    def __next__(self):
        return self.next()
    pass


class HTLBRIterator(PyexcelIterator):
    """
    Horizontal Top Left to Bottom Right Iterator

    Iterate horizontally from top left to bottom right.
    see :func:`Matrix.enumerate` for more details
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0
        self.columns = reader.number_of_columns()
        self.rows = reader.number_of_rows()
        self.total = self.columns * self.rows

    def __iter__(self):
        return self

    def next_cell_position(self):
        """
        Determine next cell position
        """
        return (int(self.current / self.columns),
                int(self.current % self.columns))

    def move_cursor(self):
        """
        move internal cursor
        """
        self.current += 1

    def get_next_value(self):
        """
        Get next value
        """
        row, column = self.next_cell_position()
        self.move_cursor()
        return self.reader_ref.cell_value(row, column)

    def exit_condition(self):
        """
        Determine if all data have been iterated
        """
        return self.current >= self.total

    def next(self):
        """
        determine next value

        this function is further divided into small functions
        so that other kind of iterators can easily change
        its behavior
        """
        if self.exit_condition():
            raise StopIteration
        else:
            return self.get_next_value()


class VTLBRIterator(HTLBRIterator):
    """
    Vertical Top Left to Bottom Right Iterator

    Iterate vertically from top left to bottom right
    see :func:`Matrix.vertical` for more details
    """
    def next_cell_position(self):
        """
        this function controls the iterator's path
        """
        return (int(self.current % self.rows),
                int(self.current / self.rows))


class HBRTLIterator(HTLBRIterator):
    """
    Horizontal Bottom Right to Top Left Iterator

    Iterate horizontally from bottom right to top left
    see :func:`Matrix.reverse` for more details
    """

    def __init__(self, reader):
        self.reader_ref = reader
        self.columns = reader.number_of_columns()
        self.rows = reader.number_of_rows()
        self.current = self.rows * self.columns

    def exit_condition(self):
        return self.current <= 0

    def move_cursor(self):
        self.current -= 1

    def get_next_value(self):
        self.move_cursor()
        row, column = self.next_cell_position()
        return self.reader_ref.cell_value(row, column)


class VBRTLIterator(HBRTLIterator):
    """
    Vertical Bottom Right to Top Left Iterator

    Iterate vertically from bottom right to top left
    see :func:`Matrix.rvertical` for more details
    """
    def next_cell_position(self):
        return (int(self.current % self.rows),
                int(self.current / self.rows))


class HTRBLIterator(PyexcelIterator):
    """
    Horizontal Top Right to Bottom Left Iterator

    Iterate horizontally from top right to bottom left::

        <<S
        <<<
        E<<
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.columns = reader.number_of_columns()
        self.rows = reader.number_of_rows()
        self.total = self.rows * self.columns
        self.row = 0
        self.column = self.columns

    def __iter__(self):
        return self

    def get_next_value(self):
        self.column -= 1
        if self.column == -1:
            self.column = self.columns - 1
            self.row += 1
        return self.reader_ref.cell_value(self.row, self.column)

    def exit_condition(self):
        return self.column == 0 and self.row == (self.rows - 1)

    def next(self):
        if self.exit_condition():
            raise StopIteration
        else:
            return self.get_next_value()


class VTRBLIterator(HTRBLIterator):
    """
    Vertical Top Right to Bottom Left Iterator

    Iterate horizontally from top left to bottom right::

        ||S
        |||
        E||
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.columns = reader.number_of_columns()
        self.rows = reader.number_of_rows()
        self.total = self.rows * self.columns
        self.row = -1
        self.column = self.columns - 1

    def get_next_value(self):
        self.row += 1
        if self.row >= self.rows:
            self.column -= 1
            self.row = 0
        return self.reader_ref.cell_value(self.row, self.column)


class VBLTRIterator(HTRBLIterator):
    """
    Vertical Bottom Left to Top Right Iterator

    Iterate vertically from bottom left to top right::

        ^^E
        ^^^
        S^^
        ->
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.columns = reader.number_of_columns()
        self.rows = reader.number_of_rows()
        self.total = self.rows * self.columns
        self.row = self.rows
        self.column = 0

    def __iter__(self):
        return self

    def get_next_value(self):
        self.row -= 1
        if self.row == -1:
            self.row = self.rows - 1
            self.column += 1
        return self.reader_ref.cell_value(self.row, self.column)

    def exit_condition(self):
        return self.row == 0 and self.column == (self.columns - 1)


class HBLTRIterator(VBLTRIterator):
    """
    Horizontal Bottom Left to Top Right Iterator

    Iterate horizontally from bottom left to top right
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.columns = reader.number_of_columns()
        self.rows = reader.number_of_rows()
        self.total = self.rows * self.columns
        self.row = self.rows - 1
        self.column = -1

    def __iter__(self):
        return self

    def get_next_value(self):
        self.column += 1
        if self.column >= self.columns:
            self.row -= 1
            self.column = 0
        return self.reader_ref.cell_value(self.row, self.column)


class RowIterator(PyexcelIterator):
    """
    Iterate data row by row from top to bottom

    default iterator for :class:`Matrix`.
    See :func:`Matrix.rows` for more details
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current in self.reader_ref.row_range():
            row = self.current
            self.current += 1
            return self.reader_ref.row_at(row)
        else:
            raise StopIteration


class RowReverseIterator(PyexcelIterator):
    """
    Iterate data row by row from bottom to top

    see :func:`Matrix.rrows` for more details
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = reader.number_of_rows() - 1

    def __iter__(self):
        return self

    def next(self):
        if self.current in self.reader_ref.row_range():
            self.current -= 1
            return self.reader_ref.row_at(self.current+1)
        else:
            raise StopIteration


class ColumnIterator(PyexcelIterator):
    """
    Column Iterator from left to right

    see :func:`Matrix.columns` for more details
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current in self.reader_ref.column_range():
            self.current += 1
            return self.reader_ref.column_at(self.current-1)
        else:
            raise StopIteration


class ColumnReverseIterator(PyexcelIterator):
    """
    Column Reverse Iterator from right to left

    see :func:`Matrix.rcolumns` for more details
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = reader.number_of_columns() - 1

    def __iter__(self):
        return self

    def next(self):
        if self.current in self.reader_ref.column_range():
            self.current -= 1
            return self.reader_ref.column_at(self.current+1)
        else:
            raise StopIteration


class ColumnIndexIterator(PyexcelIterator):
    """
    Column Iterator

    Default iterator for :class:`Sheet` when it becomes Series
    See :func:`Sheet.__iter__` for more details
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current in self.reader_ref.column_range():
            index = self.current
            self.current += 1
            column_header = self.reader_ref.colnames[index]
            return {
                column_header: self.reader_ref.named_column_at(column_header)}
        else:
            raise StopIteration


class RowIndexIterator(PyexcelIterator):
    """
    Row Iterator

    Default iterator for :class:`Sheet` when it becomes Series
    See :func:`Sheet.__iter__` for more details
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current in self.reader_ref.row_range():
            index = self.current
            self.current += 1
            column_header = self.reader_ref.rownames[index]
            return {
                column_header: self.reader_ref.named_row_at(column_header)}
        else:
            raise StopIteration


class SheetIterator(PyexcelIterator):
    """
    Sheet Iterator
    """
    def __init__(self, bookreader):
        self.book_reader_ref = bookreader
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current < self.book_reader_ref.number_of_sheets():
            self.current += 1
            return self.book_reader_ref[self.current-1]
        else:
            raise StopIteration
