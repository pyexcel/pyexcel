import random

from pyexcel.internal.sheets._shared import excel_cell_position

from .base import PyexcelSheetBase


class TestSheetAccess(PyexcelSheetBase):
    @staticmethod
    def get_random_char():
        i = random.randint(97, 122)
        return chr(i)
        
    def test_out_of_bounds_write(self):
        value = self.get_random_char()
        column = self.get_random_char() + self.get_random_char()
        cell = column + str(random.randint(9, 30))
        self.sheet[cell] = value

        self.assertEqual(value, self.sheet[cell])

    def test_out_of_column_bound_write(self):
        value = self.get_random_char()
        column = self.get_random_char() + self.get_random_char()
        cell = "A" + column + str(random.randint(9, 30))
        self.sheet[cell] = value

        self.assertEqual(value, self.sheet[cell])

    def test_out_of_bounds_read(self):
        with self.assertRaises(IndexError):
            self.sheet[0, 20]

        with self.assertRaises(IndexError):
            self.sheet[20, 0]

    def test_column_edge_case(self):
        column = self.sheet.number_of_columns() - 1

        self.assertEqual(self.sheet[0, column], f"0_{column}")
        with self.assertRaises(IndexError):
            self.sheet[0, column + 1]

    def test_row_edge_case(self):
        row = self.sheet.number_of_rows() - 1

        self.assertEqual(self.sheet[row, 0], f"{row}_0")
        with self.assertRaises(IndexError):
            self.sheet[row + 1, 0]
