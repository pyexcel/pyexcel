import os
import pyexcel as pe


class TestCSVZip:
    def setUp(self):
        self.testfile = "test3.csvz"

    def test_write_and_read(self):
        data = [[11, 112], [312, 534]]
        sheet = pe.Sheet(data)
        sheet.save_as(self.testfile)
        sheet2 = pe.load(self.testfile)
        sheet2.format(int)
        result = sheet2.to_array()
        assert data == result

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestTSVZip:
    def setUp(self):
        self.testfile = "test3.tsvz"

    def test_write_and_read(self):
        data = [[11, 112], [312, 534]]
        sheet = pe.Sheet(data)
        sheet.save_as(self.testfile)
        sheet2 = pe.load(self.testfile)
        sheet2.format(int)
        result = sheet2.to_array()
        assert data == result

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
