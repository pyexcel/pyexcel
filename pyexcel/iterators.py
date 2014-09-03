class HTLBRIterator:
    """
    Iterate horizontally from top left to bottom right
    """
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = 0
        self.total = reader.number_of_rows() * reader.number_of_columns()

    def __iter__(self):
        return self

    def next_cell_position(self):
        return (self.current / self.reader_ref.number_of_columns(),
                self.current % self.reader_ref.number_of_columns())

    def move_cursor(self):
        self.current += 1

    def get_next_value(self):
        row, column = self.next_cell_position()
        self.move_cursor()
        return self.reader_ref.cell_value(row, column)

    def exit_condition(self):
        return self.current >= self.total
        
    def next(self):
        if self.exit_condition():
            raise StopIteration
        else:
            return self.get_next_value()


class VTLBRIterator(HTLBRIterator):
    """
    Iterate vertically from top left to bottom right
    """
    def next_cell_position(self):
        return (self.current % self.reader_ref.number_of_rows(),
                self.current / self.reader_ref.number_of_rows())

class HBRTLIterator(HTLBRIterator):
    """
    Iterate horizontally from bottom right to top left
    """
    
    def __init__(self, reader):
        self.reader_ref = reader
        self.current = reader.number_of_rows() * reader.number_of_columns()

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
        return (self.current % self.reader_ref.number_of_rows(),
                self.current / self.reader_ref.number_of_rows())
