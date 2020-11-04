import unittest

import pyexcel
import random


class SheetAccessTest(unittest.TestCase):
    filename = "fixtures/non-uniform-rows.csv"

    def setUp(self):
        self.sheet = pyexcel.get_sheet(file_name=self.filename)

    @staticmethod
    def get_random_char():
        i = random.randint(97, 122)
        return chr(i)

    def test_out_of_bounds_access(self):
        value = self.get_random_char()
        column = self.get_random_char() + self.get_random_char()
        cell = column + str(random.randint(1, 30))
        self.sheet[cell] = value

        self.assertEqual(value, self.sheet[cell])
