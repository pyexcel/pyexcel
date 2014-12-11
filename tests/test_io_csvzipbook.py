import os
import pyexcel as pe
import zipfile
from _compact import OrderedDict

class TestCSVZFromFile:
    """The fixture here is a test csv file with the following data
        data = [[1, 4, 9], [2, 5, 8], [3, 6, 7]]
    was zipped to provide test-single.csvz

    then was copied three times and its three copies were zipped to form
    test-multiple.csvz.
    """

    
    def test_read_custom_made_csvz(self):
        data = [[1, 4, 9], [2, 5, 8], [3, 6, 7]]
        sheet = pe.load(os.path.join("tests", "fixtures", "test-single.csvz"))
        sheet.format(int)
        result = sheet.to_array()
        assert data == result

    def test_read_custom_made_csvz_multiple_hseet(self):
        data = [[1, 4, 9], [2, 5, 8], [3, 6, 7]]
        book = pe.load_book(os.path.join("tests", "fixtures", "test-multiple.csvz"))
        assert book.sheet_names() == ["sheet1", "sheet2", "sheet3"]
        book[0].format(int)
        book[1].format(int)
        book[2].format(int)
        assert data == book[0].to_array()
        assert data == book[1].to_array()
        assert data == book[2].to_array()


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

    def test_check_saved_file_name(self):
        data = [[11, 112], [312, 534]]
        sheet = pe.Sheet(data)
        sheet.save_as(self.testfile)
        zip = zipfile.ZipFile(self.testfile, 'r')
        list_of_files = zip.namelist()
        assert list_of_files == ['pyexcel.csv']

    def test_file_in_the_csvz_has_csv_extension(self):
        data = OrderedDict()
        data["sheet1"] = [[1,2,3]]
        data["sheet2"] = [[1,2,3]]
        data["sheet3"] = [[1,2,3]]
        book = pe.Book(data)
        book.save_as(self.testfile)
        zip = zipfile.ZipFile(self.testfile, 'r')
        list_of_files = zip.namelist()
        assert list_of_files == ['sheet1.csv', 'sheet2.csv', 'sheet3.csv']

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
