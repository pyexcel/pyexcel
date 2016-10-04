"""
    pyexcel.iterators
    ~~~~~~~~~~~~~~~~~~~

    Iterate through the two dimensional arrays

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""


class PyexcelIterator:
    """
    A parent class is used to distiguish pyexcel iterators in pyexcel utilities
    """
    def __next__(self):
        return self.next()


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
