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

    def test_update_a_column(self):
        custom_column = {"Z": [33,44,55,66,77]}
        pyexcel.processings.update_a_column(self.testfile, custom_column)
        r = pyexcel.HatReader("pyexcel_%s" % self.testfile)
        data = pyexcel.utils.to_dict(r)
        assert data["Z"] == custom_column["Z"]
        
    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
            auto_gen_file = "pyexcel_%s" % self.testfile
            os.unlink(auto_gen_file)