import pyexcel

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
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_one_dimensional_array(r)
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)