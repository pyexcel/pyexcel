import pyexcel as pe
from _compact import OrderedDict
from nose.tools import raises


class TestTutorial05:
    def test_tutorial05_example1(self):
        content="Column 1,Column 2,Column 3\n1,4,7\n2,5,8\n3,6,9"
        reader = pe.SeriesReader(("csv", content))
        reader.column["Column 2"] = [11, 12, 13]
        assert reader.column["Column 2"] == [11, 12, 13]

    @raises(ValueError)
    def test_tutorial05_example2(self):
        content="Column 1,Column 2,Column 3\n1,4,7\n2,5,8\n3,6,9"
        reader = pe.SeriesReader(("csv", content))
        del reader.column["Column 2"]
        reader.column["Column 2"]  # already deleted, bang
 
    def test_tutorial05_example3(self):
        content="Column 1,Column 2,Column 3\n1,4,7\n2,5,8\n3,6,9"
        reader = pe.SeriesReader(("csv", content))
        print(reader.column["Column 3"]) 
        extra_data = OrderedDict()
        extra_data.update({"Column 4":[10, 11, 12]})
        extra_data.update({"Column 5":[13, 14, 15]})
        reader.column += extra_data
        print(pe.utils.to_dict(reader))
        assert reader.column["Column 4"] == [10, 11, 12]
        assert reader.column["Column 5"] == [13, 14, 15]
