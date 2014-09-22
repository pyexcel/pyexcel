import pyexcel
import os


class TestCookbook:
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.ods"
        self.content = {
            "X": [1, 2, 3, 4, 5],
            "Y": [6, 7, 8, 9, 10],
            "Z": [11, 12, 13, 14, 15],
        }
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        self.testfile2 = "test.csv"
        self.content2 = {
            "O": [1, 2, 3, 4, 5],
            "P": [6, 7, 8, 9, 10],
            "Q": [11, 12, 13, 14, 15],
        }
        w = pyexcel.Writer(self.testfile2)
        w.write_dict(self.content2)
        w.close()
        self.testfile3 = "test.xls"
        self.content3 = {
            "R": [1, 2, 3, 4, 5],
            "S": [6, 7, 8, 9, 10],
            "T": [11, 12, 13, 14, 15],
        }
        w = pyexcel.Writer(self.testfile3)
        w.write_dict(self.content3)
        w.close()
        self.testfile4 = "multiple_sheets.xls"
        self.content4 = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        w = pyexcel.BookWriter(self.testfile4)
        w.write_book_from_dict(self.content4)
        w.close()

    def _test_update_columns(self):
        bad_column = {"A": [31, 1, 1, 1, 1]}
        custom_column = {"Z": [33, 44, 55, 66, 77]}
        try:
            # try non-existent column first
            pyexcel.cookbook.update_columns(self.testfile, bad_column)
            assert 1==2
        except IndexError:
            assert 1==1
        pyexcel.cookbook.update_columns(self.testfile, custom_column)
        r = pyexcel.SeriesReader("pyexcel_%s" % self.testfile)
        data = pyexcel.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]
        try:
            pyexcel.cookbook.update_columns(self.testfile, custom_column)
            r = pyexcel.SeriesReader("pyexcel_%s" % self.testfile)
            assert 1==2
        except NotImplementedError:
            assert 1==1
        pyexcel.cookbook.update_columns(self.testfile, custom_column, "test4.ods")
        r = pyexcel.SeriesReader("test4.ods")
        data = pyexcel.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]

    def test_merge_two_files(self):
        merged = pyexcel.cookbook.SHEET(self.testfile) + pyexcel.cookbook.SHEET(self.testfile2)
        import pdb; pdb.set_trace()
        r = pyexcel.SeriesReader(merged)
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content
        try:
            pyexcel.cookbook.merge_two_files(self.testfile, self.testfile2)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def _test_merge_files(self):
        file_array = [self.testfile, self.testfile2, self.testfile3]
        pyexcel.cookbook.merge_files(file_array)
        r = pyexcel.SeriesReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        content.update(self.content3)
        assert data == content
        try:
            pyexcel.cookbook.merge_files(file_array)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def _test_merge_two_readers(self):
        r1 = pyexcel.SeriesReader(self.testfile)
        r2 = pyexcel.SeriesReader(self.testfile2)
        pyexcel.cookbook.merge_two_readers(r1, r2)
        r = pyexcel.SeriesReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content
        try:
            pyexcel.cookbook.merge_two_readers(r1, r2)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def _test_merge_readers(self):
        r1 = pyexcel.SeriesReader(self.testfile)
        r2 = pyexcel.SeriesReader(self.testfile2)
        r3 = pyexcel.SeriesReader(self.testfile3)
        file_array = [r1, r2, r3]
        pyexcel.cookbook.merge_readers(file_array)
        r = pyexcel.SeriesReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        content.update(self.content3)
        assert data == content
        try:
            pyexcel.cookbook.merge_readers(file_array)
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
        if os.path.exists(self.testfile3):
            os.unlink(self.testfile3)
        if os.path.exists(self.testfile4):
            os.unlink(self.testfile4)
        auto_gen_file = "pyexcel_%s" % self.testfile
        if os.path.exists(auto_gen_file):
            os.unlink(auto_gen_file)
        another_gen_file = "pyexcel_merged.csv"
        if os.path.exists(another_gen_file):
            os.unlink(another_gen_file)
        another_gen_file = "merged.xlsx"
        if os.path.exists(another_gen_file):
            os.unlink(another_gen_file)
        another_gen_file = "merged.xls"
        if os.path.exists(another_gen_file):
            os.unlink(another_gen_file)
        another_gen_file = "test4.ods"
        if os.path.exists(another_gen_file):
            os.unlink(another_gen_file)
