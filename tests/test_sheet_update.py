import pyexcel
import os
import datetime


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
        data=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

    def test_update_a_cell(self):
        r = pyexcel.readers.PlainReader(self.testfile)
        r.cell_value(0,0,'k')
        assert r[0][0] == 'k'
        d = datetime.date(2014, 10, 1)
        r.cell_value(0,1,d)
        assert isinstance(r[0][1], datetime.date) is True
        assert r[0][1].strftime("%d/%m/%y") == "01/10/14"

    def test_update_a_cell_with_a_filter(self):
        """
        Filter the sheet first and then update the filtered now

        with the filter, you can set its value. then clear
        the filters, the value stays with the cell. so if you want
        to save the change with original data, please clear the filter
        first
        """
        r = pyexcel.FilterableReader(self.testfile)
        r.filter(pyexcel.filters.ColumnFilter([0, 2]))
        r.cell_value(2, 1, "k")
        assert r[2][1] == "k"
        r.clear_filters()
        assert r[2][3] == "k"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
