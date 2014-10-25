import os
import six
import pyexcel
if six.PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO, StringIO
from base import create_sample_file1


class TestIO:
    def test_wrong_io_input(self):
        try:
            r = pyexcel.Reader(1000)
            assert 1==2
        except IOError:
            assert 1==1

    def test_wrong_io_output(self):
        try:
            r = pyexcel.Writer(1000)
            assert 1==2
        except IOError:
            assert 1==1

    def test_not_supported_input_stream(self):
        try:
            content = "11\n11"
            r = pyexcel.Reader(("sylk", StringIO(content)))
            assert 1==2
        except NotImplementedError:
            assert 1==1

    def test_not_supported_output_stream(self):
        try:
            io = StringIO
            r = pyexcel.Writer(("sylk", io))
            assert 1==2
        except NotImplementedError:
            assert 1==1
        
    def test_csv_stringio(self):
        csvfile = "cute.csv"
        create_sample_file1(csvfile)
        with open(csvfile, "r") as f:
            content = f.read()
            r = pyexcel.Reader(("csv", StringIO(content)))
            result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
            actual = pyexcel.utils.to_array(r.enumerate())
            assert result == actual
        if os.path.exists(csvfile):
            os.unlink(csvfile)

    def test_xls_stringio(self):
        csvfile = "cute.xls"
        create_sample_file1(csvfile)
        with open(csvfile, "rb") as f:
            content = f.read()
            r = pyexcel.Reader(("xls", content))
            result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
            actual = pyexcel.utils.to_array(r.enumerate())
            assert result == actual
        if os.path.exists(csvfile):
            os.unlink(csvfile)

    def test_csv_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = StringIO()
        w = pyexcel.Writer(("csv",io))
        w.write_rows(data)
        #w.close()
        io.seek(0)
        r = pyexcel.Reader(("csv", io))
        result=[1, 2, 3, 4, 5, 6]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert actual == result

    def test_xls_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = BytesIO()
        w = pyexcel.Writer(("xls",io))
        w.write_rows(data)
        w.close()
        r = pyexcel.Reader(("xls", io.getvalue()))
        result=[1, 2, 3, 4, 5, 6]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual