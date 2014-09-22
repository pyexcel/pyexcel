import pyexcel
import os

class TestUtils():
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.csv"
        w = pyexcel.Writer(self.testfile)
        for i in [0,4,8]:
            array = [i+1, i+2, i+3, i+4]
            w.write_row(array)
        w.close()

    def test_to_one_dimension_array(self):
        r = pyexcel.Reader(self.testfile)
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pyexcel.utils.to_one_dimensional_array(r)
        assert result == actual
        actual2 = pyexcel.utils.to_one_dimensional_array(result)
        assert actual2 == result

    def test_to_dict(self):
        """
        Note: data file with column headers are tested
        in test_filters.py
        """
        r = pyexcel.Reader(self.testfile)
        result = {
            "Series_1": [1, 2, 3, 4],
            "Series_2": [5, 6, 7, 8, ],
            "Series_3": [9, 10, 11, 12]
        }
        actual = pyexcel.utils.to_dict(r.rows())
        assert result == actual
        result = {
            "Series_1": 1,
            "Series_2": 2,
            "Series_3": 3,
            "Series_4": 4,
            "Series_5": 5,
            "Series_6": 6,
            "Series_7": 7,
            "Series_8": 8,
            "Series_9": 9,
            "Series_10": 10,
            "Series_11": 11,
            "Series_12": 12
        }
        actual = pyexcel.utils.to_dict(r.enumerate())
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestUtils2():
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.xls"
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        w = pyexcel.BookWriter(self.testfile)
        w.write_book_from_dict(self.content)
        w.close()

    def test_book_reader_to_dict(self):
        r = pyexcel.BookReader(self.testfile)
        actual = pyexcel.utils.to_dict(r)
        print actual
        assert actual == self.content

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

class TestToRecord():
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "test.xls"
        self.content = {
            "X": [1, 2, 3],
            "Y": [4, 5, 6],
            "Z": [7, 8, 9]
        }
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()

    def test_book_reader_to_records(self):
        r = pyexcel.Reader(self.testfile)
        result = [
            {u'Y': 4.0, u'X': 1.0, u'Z': 7.0},
            {u'Y': 5.0, u'X': 2.0, u'Z': 8.0},
            {u'Y': 6.0, u'X': 3.0, u'Z': 9.0}]
        actual = pyexcel.utils.to_records(r)
        print actual
        assert actual == result

    def test_book_reader_to_records_with_wrong_args(self):
        r = pyexcel.BookReader(self.testfile)
        try:
            pyexcel.utils.to_records(r)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
