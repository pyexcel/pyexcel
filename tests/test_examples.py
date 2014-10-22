import pyexcel
from StringIO import StringIO


class TestTutorial05:
    def test_tutorial05_example1(self):
        content="""Column 1,Column 2,Column 3
        1,4,7
        2,5,8
        3,6,9
        """
        reader = pyexcel.SeriesReader(("csv", StringIO(content)))
        reader.column["Column 2"] = [11, 12, 13]
        assert reader.column["Column 2"] == [11, 12, 13]