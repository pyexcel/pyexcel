class HTLBRIterator:
    """
    Iterate horizontally from top left to bottom right

    default iterator for Reader class
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
        return (self.current / self.columns,
                self.current % self.columns)

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
    Iterate vertically from top left to bottom right
    """
    def next_cell_position(self):
        """
        this function controls the iterator's path
        """
        return (self.current % self.rows,
                self.current / self.rows)

class HBRTLIterator(HTLBRIterator):
    """
    Iterate horizontally from bottom right to top left
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
    Iterate vertically from bottom right to top left
    """
    def next_cell_position(self):
        return (self.current % self.rows,
                self.current / self.rows)

class HTRBLIterator:
    """
    Horizontal Top Right to Bottom Left Iterator
    
    Iterate horizontally from top right to bottom left
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
    
    Iterate horizontally from top left to bottom right
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
    
    Iterate vertically from bottom left to top right
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
    >>E
    >>> ^
    S>> |
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


class RowIterator:
    """
    Iterate data row by row from top to bottom
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

class RowReverseIterator:
    """
    Iterate data row by row from bottom to top
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

class ColumnIterator:
    """
    Column Iterator from left to right
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


class ColumnReverseIterator:
    """
    Column Reverse Iterator from right to left
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


class SeriesColumnIterator:
    """
    Column Iterator
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0
        self.headers = reader.series()

    def __iter__(self):
        return self

    def next(self):
        if self.current in self.reader_ref.column_range():
            self.current += 1
            return self.reader_ref.named_column_at(self.headers[self.current-1])
        else:
            raise StopIteration
