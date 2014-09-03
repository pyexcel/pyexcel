class HorizontalIterator:
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0
        self.total = reader.number_of_rows() * reader.number_of_columns()

    def __iter__(self):
        return self

    def next(self):
        if self.current >= self.total:
            raise StopIteration
        else:
            row = self.current / self.reader_ref.number_of_columns()
            column = self.current % self.reader_ref.number_of_columns()
            self.current += 1
            return self.reader_ref.cell_value(row, column)

class VerticalIterator(HorizontalIterator):
    def next(self):
        if self.current >= self.total:
            raise StopIteration
        else:
            row = self.current % self.reader_ref.number_of_rows()
            column = self.current / self.reader_ref.number_of_rows()
            self.current += 1
            return self.reader_ref.cell_value(row, column)

class HorizontalReverseIterator:
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = reader.number_of_rows() * reader.number_of_columns()

    def __iter__(self):
        return self

    def next(self):
        if self.current <= 0:
            raise StopIteration
        else:
            self.current -= 1
            row = self.current / self.reader_ref.number_of_columns()
            column = self.current % self.reader_ref.number_of_columns()
            return self.reader_ref.cell_value(row, column)

class VerticalReverseIterator(HorizontalReverseIterator):
    def next(self):
        if self.current <=0:
            raise StopIteration
        else:
            self.current -= 1
            row = self.current % self.reader_ref.number_of_rows()
            column = self.current / self.reader_ref.number_of_rows()
            return self.reader_ref.cell_value(row, column)
