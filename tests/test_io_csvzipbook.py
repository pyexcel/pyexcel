import os
import pyexcel as pe


class TestCSVZFromFile:

    def test_write_and_read(self):
        data = [[1, 4, 9], [2, 5, 8], [3, 6, 7]]
        sheet = pe.load(os.path.join("tests", "fixtures", "test-single.csvz"))
        sheet.format(int)
        result = sheet.to_array()
        print result
        assert data == result


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
