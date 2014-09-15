import pyexcel
import json
import os

def to_json(iterator):
    array = pyexcel.utils.to_array(iterator)
    return json.dumps(array)


class PyexcelWriterBase:
    """
    Abstract functional test for writers

    testfile and testfile2 have to be initialized before
    it is used for testing
    """
    content = [
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5]
    ]
    
    def test_write_array(self):
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()
        r = pyexcel.Reader(self.testfile)
        actual = pyexcel.utils.to_array(r.rows())
        assert actual == self.content

    def test_write_reader(self):
        """
        Use reader as data container

        this test case shows the file written by pyexcel
        can be read back by itself
        """
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()
        r = pyexcel.Reader(self.testfile)
        w2 = pyexcel.Writer(self.testfile2)
        w2.write_reader(r)
        w2.close()
        r2 = pyexcel.Reader(self.testfile2)
        actual = pyexcel.utils.to_array(r2.rows())
        assert actual == self.content


class PyexcelHatWriterBase:
    """
    Abstract functional test for hat writers
    """
    content = {
        "X": [1,2,3,4,5],
        "Y": [6,7,8,9,10],
        "Z": [11,12,13,14,15],
    }
    
    def test_series_table(self):
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        r = pyexcel.SeriesReader(self.testfile)
        actual = pyexcel.utils.to_dict(r)
        assert actual == self.content
    

class PyexcelBase:
    def _write_test_file(self, file):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.rows = 3
        w = pyexcel.Writer(file)
        for i in range(0,self.rows):
            row = i + 1
            array = [row, row, row, row]
            w.write_row(array)
        w.close()
        
    def test_number_of_rows(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == r.number_of_rows()

    def test_cell_value(self):
        r = pyexcel.Reader(self.testfile)
        for i in range(0, self.rows):
            row = i + 1
            assert row == r.cell_value(i,1)
        for i in r.row_range():
            print r.cell_value(i,1)
            assert i+1 == r.cell_value(i,1)
        assert 3 == r.cell_value(2, 3)
            
    def test_row_range(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == len(r.row_range())
            
    def test_number_of_columns(self):
        r = pyexcel.Reader(self.testfile)
        assert 4 == r.number_of_columns()

    def test_json(self):
        r = pyexcel.Reader(self.testfile)
        assert to_json(r.rows()) == '[[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]'

class PyexcelXlsBase(PyexcelBase):

    def test_json(self):
        r = pyexcel.Reader(self.testfile)
        assert to_json(r.rows()) == '[[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0], [3.0, 3.0, 3.0, 3.0]]'


class PyexcelMultipleSheetBase:

    def test_sheet_names(self):
        r = pyexcel.Reader(os.path.join("tests", self.testfile))
        expected = [ "Sheet1", "Sheet2", "Sheet3"]
        sheet_names = r.sheet_names()
        print sheet_names
        for name in sheet_names:
            assert name in expected

    def test_number_of_sheets(self):
        r = pyexcel.Reader(os.path.join("tests", self.testfile))
        assert r.number_of_sheets() == 3

    def test_reading_through_sheets(self):
        r = pyexcel.Reader(os.path.join("tests", self.testfile))
        data = pyexcel.utils.to_array(r.rows())
        expected = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
        assert data == expected
        r.use_sheet_at_index(1)
        data = pyexcel.utils.to_array(r.rows())
        expected = [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]
        assert data == expected
        r.use_sheet_at_index(2)
        data = pyexcel.utils.to_array(r.rows())
        expected = [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected
        
