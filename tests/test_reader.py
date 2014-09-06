import pyexcel
import os

class TestReader:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        w = pyexcel.Writer(self.testfile)
        data=['a','b','c','d','e','f','g','h','i','j',1.1,1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

    def test_cell_value(self):
        r = pyexcel.Reader(self.testfile)
        value = r.cell_value(100,100)
        assert value == None

    def test_row_at(self):
        r = pyexcel.Reader(self.testfile)
        value = r.row_at(100)
        assert value == None
        value = r.row_at(2)
        assert value == ['i', 'j', 1.1, 1]
        
    def test_column_at(self):
        r = pyexcel.Reader(self.testfile)
        value = r.column_at(100)
        assert value == None
        value = r.column_at(1)
        assert value == ['b','f','j']

    def test_not_supported_file(self):
        try:
            r = pyexcel.Reader("test.sylk")
            assert 0==1
        except NotImplementedError:
            assert 1==1

    def test_contains(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda row: row[0]=='a' and row[1] == 'b'
        assert r.contains(f) == True
        

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
