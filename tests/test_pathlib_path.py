import os
from pathlib import Path

import pyexcel as pe

from nose.tools import eq_


class TestiGetArray:
    def setUp(self):
        self.test_data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]

    def tearDown(self):
        pe.free_resources()

    def test_get_array_from_file(self):
        sheet = pe.Sheet(self.test_data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.iget_array(file_name=Path(testfile))
        eq_(list(result), self.test_data)
        os.unlink(testfile)
