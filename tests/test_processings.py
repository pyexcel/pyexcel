import pyexcel
import os


class TestProcessings:
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.ods"
        self.content = {
            "X": [1,2,3,4,5],
            "Y": [6,7,8,9,10],
            "Z": [11,12,13,14,15],
        }
        w = pyexcel.Writer(self.testfile)
        w.write_hat_table(self.content)
        w.close()
        self.testfile2 = "test.csv"
        self.content2 = {
            "O": [1,2,3,4,5],
            "P": [6,7,8,9,10],
            "Q": [11,12,13,14,15],
        }
        w = pyexcel.Writer(self.testfile2)
        w.write_hat_table(self.content2)
        w.close()
        self.testfile3 = "test.xls"
        self.content3 = {
            "R": [1,2,3,4,5],
            "S": [6,7,8,9,10],
            "T": [11,12,13,14,15],
        }
        w = pyexcel.Writer(self.testfile3)
        w.write_hat_table(self.content3)
        w.close()

    def test_update_a_column(self):
        custom_column = {"Z": [33,44,55,66,77]}
        pyexcel.processings.update_a_column(self.testfile, custom_column)
        r = pyexcel.HatReader("pyexcel_%s" % self.testfile)
        data = pyexcel.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]

    def test_merge_two_files(self):
        pyexcel.processings.merge_two_files(self.testfile, self.testfile2)
        r = pyexcel.HatReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content
        
    def test_merge_files(self):
        file_array = [self.testfile, self.testfile2, self.testfile3]
        pyexcel.processings.merge_files(file_array)
        r = pyexcel.HatReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        content.update(self.content3)
        assert data == content
        
    def test_merge_two_readers(self):
        r1 = pyexcel.HatReader(self.testfile)
        r2 = pyexcel.HatReader(self.testfile2)
        pyexcel.processings.merge_two_readers(r1, r2)
        r = pyexcel.HatReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        assert data == content
        
    def test_merge_readers(self):
        r1 = pyexcel.HatReader(self.testfile)
        r2 = pyexcel.HatReader(self.testfile2)
        r3 = pyexcel.HatReader(self.testfile3)
        file_array = [r1, r2, r3]
        pyexcel.processings.merge_readers(file_array)
        r = pyexcel.HatReader("pyexcel_merged.csv")
        data = pyexcel.utils.to_dict(r)
        content = {}
        content.update(self.content)
        content.update(self.content2)
        content.update(self.content3)
        assert data == content
        
    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
        if os.path.exists(self.testfile3):
            os.unlink(self.testfile3)
        auto_gen_file = "pyexcel_%s" % self.testfile
        if os.path.exists(auto_gen_file):
            os.unlink(auto_gen_file)
        another_gen_file = "pyexcel_merged.csv"
        if os.path.exists(another_gen_file):
            os.unlink(another_gen_file)