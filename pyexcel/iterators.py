"""
    pyexcel.iterators
    ~~~~~~~~~~~~~~~~~~~

    Iterate through the two dimensional arrays

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import six
import copy


def f7(seq):
    """
    Reference:
    http://stackoverflow.com/questions/480214/
    how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


class IteratableArray:
    """
    To be able to use the iterators in this package, implement
    these methods
    """
    def __init__(self, array):
        self.array = array

    def number_of_rows(self):
        return len(self.array)

    def number_of_columns(self):
        if self.number_of_rows() > 0:
            return len(self.array[0])
        else:
            return 0

    def row_range(self):
        """
        Utility function to get row range
        """
        return range(0, self.number_of_rows())

    def column_range(self):
        """
        Utility function to get column range
        """
        return range(0, self.number_of_columns())

    def cell_value(self, row, column, new_value=None):
        if new_value is None:
            if row in self.row_range() and column in self.column_range():
                # apply formatting
                return self.array[row][column]
            else:
                return None
        else:
            self.array[row][column] = new_value
            return new_value

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

    def extend_rows(self, rows):
        """expected the rows to be off the same length"""
        array_length = self.number_of_columns()
        for r in rows:
            length = len(r)
            agreed_length = min(length, array_length)
            array = copy.deepcopy(r[:agreed_length])
            if length < array_length:
                array = array + [""] * (array_length-length)
            self.array.append(array)

    def delete_rows(self, row_indices):
        """delete rows"""
        if isinstance(row_indices, list) is False:
            raise ValueError
        if len(row_indices) > 0:
            unique_list = f7(row_indices)
            sorted_list = sorted(unique_list, reverse=True)
            for i in sorted_list:
                if i < self.number_of_rows():
                    del self.array[i]

    def extend_columns(self, columns):
        """
        columns should be an array

        s s s     t t
        s s s  +  t t
        """
        current_nrows = self.number_of_rows()
        current_ncols = self.number_of_columns()
        insert_column_nrows = len(columns)
        array_length = min(current_nrows, insert_column_nrows)
        for i in range(0, array_length):
            length = len(self.array[i])
            if length < current_ncols:
                self.array[i] += [""] * (current_ncols - length)
            array = copy.deepcopy(columns[i])
            self.array[i] += array
        if current_nrows < insert_column_nrows:
            delta = insert_column_nrows - current_nrows
            base = current_nrows
            for i in range(0, delta):
                new_array = [""] * current_ncols
                new_array += columns[base+i]
                self.array.append(new_array)

    def delete_columns(self, column_indices):
        """
        Delete columns by specified list of indices
        """
        if isinstance(column_indices, list) is False:
            raise ValueError
        if len(column_indices) > 0:
            unique_list = f7(column_indices)
            sorted_list = sorted(unique_list, reverse=True)
            for i in range(0, len(self.array)):
                for j in sorted_list:
                    del self.array[i][j]

    def __delitem__(self, aslice):
        if isinstance(aslice, slice):
            if aslice.start is None:
                start = 0
            else:
                start = max(aslice.start, 0)
            if aslice.stop is None:
                stop = self.number_of_rows()
            else:
                stop = min(aslice.stop, self.number_of_rows())
            if start > stop:
                raise ValueError
            elif start < stop:
                if aslice.step:
                    my_range = range(start, stop, aslice.step)
                else:
                    my_range = range(start, stop)
                if six.PY3:
                    # for py3, my_range is a range object
                    my_range = list(my_range)
                self.delete_rows(my_range)
            else:
                # start == stop
                self.delete_rows([start])
        else:
            self.delete_rows([aslice])

    def __setitem__(self, aslice, c):
        if isinstance(aslice, slice):
            if aslice.start is None:
                start = 0
            else:
                start = max(aslice.start, 0)
            if aslice.stop is None:
                stop = self.number_of_rows()
            else:
                stop = min(aslice.stop, self.number_of_rows())
            if start > stop:
                raise ValueError
            elif start < stop:
                if aslice.step:
                    my_range = range(start, stop, aslice.step)
                else:
                    my_range = range(start, stop)
                for i in my_range:
                    self.set_row_at(i, c)
            else:
                # start == stop
                self.set_row_at(start, c)
        else:
            self.set_row_at(aslice, c)

    def __getitem__(self, aslice):
        """By default, this class recognize from top to bottom
        from left to right"""
        index = aslice
        if isinstance(aslice, slice):
            if aslice.start is None:
                start = 0
            else:
                start = max(aslice.start, 0)
            if aslice.stop is None:
                stop = self.number_of_rows()
            else:
                stop = min(aslice.stop, self.number_of_rows())
            if start > stop:
                return None
            elif start < stop:
                if aslice.step:
                    my_range = range(start, stop, aslice.step)
                else:
                    my_range = range(start, stop)
                results = []
                for i in my_range:
                    results.append(self.row_at(i))
                return results
            else:
                # drop this to index handler
                index = start
        if index in self.row_range():
            return self.row_at(index)
        else:
            raise IndexError

    def set_column_at(self, column_index, data_array, starting=0):
        nrows = self.number_of_rows()
        ncolumns = self.number_of_columns()
        if column_index < ncolumns and starting < nrows:
            to = min(len(data_array)+starting, self.number_of_rows())
            for i in range(starting, to):
                self.cell_value(i, column_index, data_array[i])
        else:
            raise ValueError

    def set_row_at(self, row_index, data_array, starting=0):
        nrows = self.number_of_rows()
        ncolumns = self.number_of_columns()
        if row_index < nrows and starting < ncolumns:
            to = min(len(data_array)+starting, self.number_of_columns())
            for i in range(starting, to):
                self.cell_value(row_index, i, data_array[i])
        else:
            raise ValueError

    def contains(self, predicate):
        for r in self.rows():
            if predicate(r):
                return True
        else:
            return False

    def transpose(self):
        from .utils import transpose
        self.array = transpose(self.array)


class PyexcelIterator:
    def __next__(self):
        return self.next()
    pass


class HTLBRIterator(PyexcelIterator):
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
    Iterate vertically from top left to bottom right
    """
    def next_cell_position(self):
        """
        this function controls the iterator's path
        """
        return (int(self.current % self.rows),
                int(self.current / self.rows))


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
        return (int(self.current % self.rows),
                int(self.current / self.rows))


class HTRBLIterator(PyexcelIterator):
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


class RowIterator(PyexcelIterator):
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


class RowReverseIterator(PyexcelIterator):
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


class ColumnIterator(PyexcelIterator):
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


class ColumnReverseIterator(PyexcelIterator):
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


class SeriesColumnIterator(PyexcelIterator):
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
            index = self.current
            self.current += 1
            return self.reader_ref.named_column_at(self.headers[index])
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
