import pyexcel
import os

class TestCSV:
    def test_bug_01(self):
        """
        if first row of csv is shorter than the rest of the rows,
        the csv will be truncated by first row. This is a bug

        "a,d,e,f" <- this will be 1
        '1',2,3,4 <- 4
        '2',3,4,5
        'b'       <- give '' for missing cells
        """
        r = pyexcel.Reader(os.path.join("tests", "fixtures", "bug_01.csv"))
        assert len(r[0]) == 4
        # test "" is append for empty cells
        assert r[0][1] == ""
        assert r[3][1] == ""
        
        