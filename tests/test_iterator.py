import os
import pyexcel

class TestIteratorWithPlainReader:
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

    def test_horizontal_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        
    def test_row_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_one_dimensional_array(r.rows())
        assert result == actual
        
    def test_row_iterator_2_dimensions(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
        actual = pyexcel.utils.to_array(r.rows())
        assert result == actual
        
    def test_horizontal_reverse_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [12,11,10,9,8,7,6,5,4,3,2,1]
        actual = pyexcel.utils.to_array(r.reverse())
        assert result == actual

    def test_row_reverse_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [9,10,11,12,5,6,7,8,1,2,3,4]
        actual = pyexcel.utils.to_one_dimensional_array(r.rrows())
        assert result == actual

    def test_row_reverse_iterator_2_dimensions(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [[9,10,11,12],[5,6,7,8],[1,2,3,4]]
        actual = pyexcel.utils.to_array(r.rrows())
        assert result == actual

    def test_vertical_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [1,5,9,2,6,10,3,7,11,4,8,12]
        actual = pyexcel.utils.to_array(r.vertical())
        assert result == actual
        
    def test_column_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [1,5,9,2,6,10,3,7,11,4,8,12]
        actual = pyexcel.utils.to_one_dimensional_array(r.columns())
        assert result == actual
        
    def test_column_iterator_2_dimensions(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [[1,5,9],[2,6,10],[3,7,11],[4,8,12]]
        actual = pyexcel.utils.to_array(r.columns())
        assert result == actual
        
    def test_vertical_reverse_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [12,8,4,11,7,3,10,6,2,9,5,1]
        actual = pyexcel.utils.to_array(r.rvertical())
        assert result == actual
        
    def test_column_reverse_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [4,8,12,3,7,11,2,6,10,1,5,9]
        actual = pyexcel.utils.to_one_dimensional_array(r.rcolumns())
        assert result == actual
        
    def test_column_reverse_iterator_2_dimensions(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [[4,8,12],[3,7,11],[2,6,10],[1,5,9]]
        actual = pyexcel.utils.to_array(r.rcolumns())
        assert result == actual
        
    def test_horizontal_top_right_2_bottom_left_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [4,3,2,1,8,7,6,5,12,11,10,9]
        actual = pyexcel.utils.to_array(pyexcel.iterators.HTRBLIterator(r))
        assert result == actual
        
    def test_horizontal_bottom_left_2_top_right_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [9,10,11,12,5,6,7,8,1,2,3,4]
        actual = pyexcel.utils.to_array(pyexcel.iterators.HBLTRIterator(r))
        assert result == actual
        
    def test_vertical_bottom_left_2_top_right_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [9,5,1,10,6,2,11,7,3,12,8,4]
        actual = pyexcel.utils.to_array(pyexcel.iterators.VBLTRIterator(r))
        assert result == actual
        
    def test_vertical_top_right_2_bottom_left_iterator(self):
        r = pyexcel.PlainReader(self.testfile)
        result = [4,8,12,3,7,11,2,6,10,1,5,9]
        actual = pyexcel.utils.to_array(pyexcel.iterators.VTRBLIterator(r))
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

class TestIterator:
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

    def test_horizontal_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        
    def test_row_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_one_dimensional_array(r.rows())
        assert result == actual
        
    def test_row_iterator_2_dimensions(self):
        r = pyexcel.Reader(self.testfile)
        result = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
        actual = pyexcel.utils.to_array(r.rows())
        assert result == actual
        
    def test_horizontal_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [12,11,10,9,8,7,6,5,4,3,2,1]
        actual = pyexcel.utils.to_array(r.reverse())
        assert result == actual

    def test_row_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [9,10,11,12,5,6,7,8,1,2,3,4]
        actual = pyexcel.utils.to_one_dimensional_array(r.rrows())
        assert result == actual

    def test_row_reverse_iterator_2_dimensions(self):
        r = pyexcel.Reader(self.testfile)
        result = [[9,10,11,12],[5,6,7,8],[1,2,3,4]]
        actual = pyexcel.utils.to_array(r.rrows())
        assert result == actual

    def test_vertical_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,5,9,2,6,10,3,7,11,4,8,12]
        actual = pyexcel.utils.to_array(r.vertical())
        assert result == actual
        
    def test_column_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,5,9,2,6,10,3,7,11,4,8,12]
        actual = pyexcel.utils.to_one_dimensional_array(r.columns())
        assert result == actual
        
    def test_column_iterator_2_dimensions(self):
        r = pyexcel.Reader(self.testfile)
        result = [[1,5,9],[2,6,10],[3,7,11],[4,8,12]]
        actual = pyexcel.utils.to_array(r.columns())
        assert result == actual
        
    def test_vertical_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [12,8,4,11,7,3,10,6,2,9,5,1]
        actual = pyexcel.utils.to_array(r.rvertical())
        assert result == actual
        
    def test_column_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [4,8,12,3,7,11,2,6,10,1,5,9]
        actual = pyexcel.utils.to_one_dimensional_array(r.rcolumns())
        assert result == actual
        
    def test_column_reverse_iterator_2_dimensions(self):
        r = pyexcel.Reader(self.testfile)
        result = [[4,8,12],[3,7,11],[2,6,10],[1,5,9]]
        actual = pyexcel.utils.to_array(r.rcolumns())
        assert result == actual
        
    def test_horizontal_top_right_2_bottom_left_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [4,3,2,1,8,7,6,5,12,11,10,9]
        actual = pyexcel.utils.to_array(pyexcel.iterators.HTRBLIterator(r))
        assert result == actual
        
    def test_horizontal_bottom_left_2_top_right_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [9,10,11,12,5,6,7,8,1,2,3,4]
        actual = pyexcel.utils.to_array(pyexcel.iterators.HBLTRIterator(r))
        assert result == actual
        
    def test_vertical_bottom_left_2_top_right_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [9,5,1,10,6,2,11,7,3,12,8,4]
        actual = pyexcel.utils.to_array(pyexcel.iterators.VBLTRIterator(r))
        assert result == actual
        
    def test_vertical_top_right_2_bottom_left_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [4,8,12,3,7,11,2,6,10,1,5,9]
        actual = pyexcel.utils.to_array(pyexcel.iterators.VTRBLIterator(r))
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestHatIterators:
    def setUp(self):
        self.testfile = "test.csv"
        self.content = [
            ["X", "Y", "Z"],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3]
        ]
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_hat_column_iterator(self):
        r = pyexcel.SeriesReader(self.testfile)
        result = pyexcel.utils.to_dict(r)
        actual = {
            "X":[1,1,1,1,1],
            "Y":[2,2,2,2,2],
            "Z":[3,3,3,3,3],
        }
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        