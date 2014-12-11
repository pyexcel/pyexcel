import pyexcel as pe
import pyexcel.ext.xls
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
        r = pe.Reader(os.path.join("tests", "fixtures", "bug_01.csv"))
        assert len(r.row[0]) == 4
        # test "" is append for empty cells
        assert r[0,1] == ""
        assert r[3,1] == ""
        
    def test_issue_03(self):
        file_prefix = "issue_03_test"
        csv_file = "%s.csv" % file_prefix
        xls_file = "%s.xls" % file_prefix
        my_sheet_name = "mysheetname"
        data = [[1,1]]
        sheet = pe.Sheet(data, name=my_sheet_name)
        sheet.save_as(csv_file)
        assert(os.path.exists(csv_file))
        sheet.save_as(xls_file)
        book = pe.load_book(xls_file)
        assert book.sheet_names()[0] == my_sheet_name
        os.unlink(csv_file)
        os.unlink(xls_file)