import pyexcel
from StringIO import StringIO


class TestTutorial05:
    def test_tutorial05_example1(self):
        content="Column 1,Column 2,Column 3\n1,4,7\n2,5,8\n3,6,9"
        reader = pyexcel.SeriesReader(("csv", StringIO(content)))
        reader.column["Column 2"] = [11, 12, 13]
        assert reader.column["Column 2"] == {"Column 2": [11, 12, 13]}

    def test_tutorial05_example2(self):
        content="Column 1,Column 2,Column 3\n1,4,7\n2,5,8\n3,6,9"
        reader = pyexcel.SeriesReader(("csv", StringIO(content)))
        del reader.column["Column 2"]
        try:
            reader.column["Column 2"]
            assert 1==2
        except ValueError:
            assert 1==1
