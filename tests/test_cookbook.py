import pyexcel
import os


class TestSpliting:
    def setUp(self):
        self.testfile4 = "multiple_sheets.xls"
        self.content4 = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        w = pyexcel.BookWriter(self.testfile4)
        w.write_book_from_dict(self.content4)
        w.close()

    def test_split_a_book(self):
        pyexcel.cookbook.split_a_book(self.testfile4, "extracted.csv")
        assert os.path.exists("Sheet1_extracted.csv")
        assert os.path.exists("Sheet2_extracted.csv")
        assert os.path.exists("Sheet3_extracted.csv")

    def test_split_a_book_2(self):
        """use default output file name"""
        pyexcel.cookbook.split_a_book(self.testfile4)
        assert os.path.exists("Sheet1_%s" % self.testfile4)
        assert os.path.exists("Sheet2_%s" % self.testfile4)
        assert os.path.exists("Sheet3_%s" % self.testfile4)

    def test_extract_a_book(self):
        pyexcel.cookbook.extract_a_sheet_from_a_book(self.testfile4, "Sheet1", "extracted.csv")
        assert os.path.exists("Sheet1_extracted.csv")

    def test_extract_a_book_2(self):
        """Use default output file name"""
        pyexcel.cookbook.extract_a_sheet_from_a_book(self.testfile4, "Sheet1")
        assert os.path.exists("Sheet1_%s" % self.testfile4)

    def tearDown(self):
        if os.path.exists(self.testfile4):
            os.unlink(self.testfile4)
        if os.path.exists("Sheet1_extracted.csv"):
            os.unlink("Sheet1_extracted.csv")
        if os.path.exists("Sheet2_extracted.csv"):
            os.unlink("Sheet2_extracted.csv")
        if os.path.exists("Sheet3_extracted.csv"):
            os.unlink("Sheet3_extracted.csv")
        if os.path.exists("Sheet1_multiple_sheets.xls"):
            os.unlink("Sheet1_multiple_sheets.xls")
        if os.path.exists("Sheet2_multiple_sheets.xls"):
            os.unlink("Sheet2_multiple_sheets.xls")
        if os.path.exists("Sheet3_multiple_sheets.xls"):
            os.unlink("Sheet3_multiple_sheets.xls")


class TestCookbook:
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test1.xls"
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

    def test_update_columns(self):
        bad_column = {"A": [31, 1, 1, 1, 1]}
        custom_column = {"Z": [33, 44, 55, 66, 77]}
        try:
            # try non-existent column first
            pyexcel.cookbook.update_columns(self.testfile, bad_column)
            assert 1==2
        except ValueError:
            assert 1==1
        pyexcel.cookbook.update_columns(self.testfile, custom_column)
        r = pyexcel.SeriesReader("pyexcel_%s" % self.testfile)
        data = pyexcel.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]
        try:
            # test if it try not overwrite a file
            pyexcel.cookbook.update_columns(self.testfile, custom_column)
            r = pyexcel.SeriesReader("pyexcel_%s" % self.testfile)
            assert 1==2
        except NotImplementedError:
            assert 1==1
        pyexcel.cookbook.update_columns(self.testfile, custom_column, "test4.xls")
        r = pyexcel.SeriesReader("test4.xls")
        data = pyexcel.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]

    def test_update_rows(self):
        bad_column = {100: [31, 1, 1, 1, 1]}
        custom_column = {1: [2,3,4]}
        try:
            # try non-existent column first
            pyexcel.cookbook.update_rows(self.testfile, bad_column)
            assert 1==2
        except ValueError:
            assert 1==1
        pyexcel.cookbook.update_rows(self.testfile, custom_column)
        r = pyexcel.Reader("pyexcel_%s" % self.testfile)
        assert custom_column[1] == r.row_at(1)
        try:
            # try not to overwrite a file
            pyexcel.cookbook.update_rows(self.testfile, custom_column)
            r = pyexcel.SeriesReader("pyexcel_%s" % self.testfile)
            assert 1==2
        except NotImplementedError:
            assert 1==1
        pyexcel.cookbook.update_rows(self.testfile, custom_column, "test4.xls")
        r = pyexcel.Reader("test4.xls")
        assert custom_column[1] == r.row_at(1)

    def test_merge_two_files(self):
        pyexcel.cookbook.merge_two_files(self.testfile, self.testfile2)
        r = pyexcel.SeriesReader("pyexcel_merged.csv")
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

    def test_merge_files(self):
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

    def test_merge_two_readers(self):
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

    def test_merge_readers(self):
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

    def test_merge_two_row_filter_hat_readers(self):
        r1 = pyexcel.SeriesReader(self.testfile)
        r2 = pyexcel.SeriesReader(self.testfile2)
        pyexcel.cookbook.merge_two_readers(r1, r2)
        r = pyexcel.SeriesReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content

    def test_merge_two_row_filter_hat_readers_2(self):
        """
        Now start row filtering
        """
        r1 = pyexcel.SeriesReader(self.testfile)
        r1.add_filter(pyexcel.filters.OddRowFilter())
        r2 = pyexcel.SeriesReader(self.testfile2)
        r2.add_filter(pyexcel.filters.EvenRowFilter())
        pyexcel.cookbook.merge_two_readers(r1, r2)
        r = pyexcel.SeriesReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {
            'Y': [7, 9, ''],
            'X': [2, 4, ''],
            'Z': [12, 14, ''],
            'O': [1, 3, 5],
            'Q': [11, 13, 15],
            'P': [6, 8, 10]
        }
        assert data == content

    def test_merge_two_row_filter_hat_readers_3(self):
        """
        Now start column filtering
        """
        r1 = pyexcel.SeriesReader(self.testfile)
        r1.add_filter(pyexcel.filters.OddColumnFilter())
        r2 = pyexcel.SeriesReader(self.testfile2)
        r2.add_filter(pyexcel.filters.EvenColumnFilter())
        pyexcel.cookbook.merge_two_readers(r1, r2)
        r = pyexcel.SeriesReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {
            "Y": [6, 7, 8, 9, 10],
            "O": [1, 2, 3, 4, 5],
            "Q": [11, 12, 13, 14, 15]
        }
        assert data == content

    def test_merge_any_files_to_a_book(self):
        file_array = [self.testfile, self.testfile2,
                      self.testfile3, self.testfile4]
        pyexcel.cookbook.merge_all_to_a_book(file_array, "merged.xlsx")
        r = pyexcel.BookReader("merged.xlsx")
        content = pyexcel.utils.to_dict(r[self.testfile].become_series())
        assert content == self.content
        content2 = pyexcel.utils.to_dict(r[self.testfile2].become_series())
        assert content2 == self.content2
        content3 = pyexcel.utils.to_dict(r[self.testfile3].become_series())
        assert content3 == self.content3
        content4 = pyexcel.utils.to_array(r["Sheet1"])
        assert content4 == self.content4["Sheet1"]
        content5 = pyexcel.utils.to_array(r["Sheet2"])
        assert content5 == self.content4["Sheet2"]
        content6 = pyexcel.utils.to_array(r["Sheet3"])
        assert content6 == self.content4["Sheet3"]

    def test_merge_csv_files_to_a_book(self):
        file_array = [self.testfile, self.testfile2,
                      self.testfile3]
        pyexcel.cookbook.merge_csv_to_a_book(file_array, "merged.xlsx")
        r = pyexcel.BookReader("merged.xlsx")
        content = pyexcel.utils.to_dict(r[self.testfile].become_series())
        assert content == self.content
        content2 = pyexcel.utils.to_dict(r[self.testfile2].become_series())
        print content2
        assert content2 == self.content2
        content3 = pyexcel.utils.to_dict(r[self.testfile3].become_series())
        assert content3 == self.content3

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
        another_gen_file = "test4.xls"
        if os.path.exists(another_gen_file):
            os.unlink(another_gen_file)
