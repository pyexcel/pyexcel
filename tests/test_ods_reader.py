import pyexcel
import os


class TestODSReader:
    def setUp(self):
        r = pyexcel.ext.odsbook.ODSReader(os.path.join("tests",
                                                       "fixtures",
                                                       "ods_formats.ods"))
        self.data = {}
        for s in r.sheet_names:
            self.data[s] = []
            for y in r.SHEETS[s]:
                my_array = []
                for x in y:
                    my_array.append(x.value)
                self.data[s].append(my_array)

    def test_formats(self):
        # date formats
        date_format = "%d/%m/%Y"
        assert self.data["Sheet1"][0][0] == "Date"
        assert self.data["Sheet1"][1][0].strftime(date_format) == "11/11/2014"
        assert self.data["Sheet1"][2][0].strftime(date_format) == "01/01/2001"
        assert self.data["Sheet1"][3][0] == ""
        # time formats
        time_format = "%S:%M:%H"
        assert self.data["Sheet1"][0][1] == "Time"
        assert self.data["Sheet1"][1][1].strftime(time_format) == "12:12:11"
        assert self.data["Sheet1"][2][1].strftime(time_format) == "12:00:00"
        assert self.data["Sheet1"][3][1] == 0
        # boolean
        assert self.data["Sheet1"][0][2] == "Boolean"
        assert self.data["Sheet1"][1][2] == True
        assert self.data["Sheet1"][2][2] == False
        # Float
        assert self.data["Sheet1"][0][3] == "Float"
        assert self.data["Sheet1"][1][3] == 11.11
        # Currency
        assert self.data["Sheet1"][0][4] == "Currency"
        assert self.data["Sheet1"][1][4] == 1
        assert self.data["Sheet1"][2][4] == -10000
        # Percentage
        assert self.data["Sheet1"][0][5] == "Percentage"
        assert self.data["Sheet1"][1][5] == 2
        # int
        assert self.data["Sheet1"][0][6] == "Int"
        assert self.data["Sheet1"][1][6] == 3
        assert self.data["Sheet1"][2][6] == ""
        assert self.data["Sheet1"][4][6] == 11
        # Scientifed not supported
        assert self.data["Sheet1"][1][7] == 100000
        # Fraction
        print self.data["Sheet1"][1][8]
        assert self.data["Sheet1"][1][8] == 1.25
        # Text
        assert self.data["Sheet1"][1][9] == "abc"