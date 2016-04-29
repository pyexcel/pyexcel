import os
from textwrap import dedent
from unittest import TestCase

import pyexcel as pe
from datetime import datetime
from _compact import StringIO, OrderedDict


class TestBugFixes(TestCase):
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

    def test_issue_06(self):
        import logging
        logger = logging.getLogger("test")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
        output = StringIO()
        book = pe.Book({'hoja1':[['datos', 'de', 'prueba'],[1, 2, 3]], })
        book.save_to_memory('csv', output)
        logger.debug(output.getvalue())
        assert 1==1

    def test_issue_09(self):
        pe.utils.LOCAL_UUID = 0
        merged = pe.Book()
        sheet1 = pe.Sheet(sheet=[[1,2]])
        sheet2 = pe.Sheet(sheet=[[1,2]])
        merged += sheet1
        merged += sheet2
        assert merged[1].name == "pyexcel_1"

    def test_issue_10(self):
        thedict = OrderedDict()
        thedict.update({"Column 1": [1,2,3]})
        thedict.update({"Column 2": [1,2,3]})
        thedict.update({"Column 3": [1,2,3]})
        pe.save_as(adict=thedict, dest_file_name="issue10.xls")
        newdict = pe.get_dict(file_name="issue10.xls")
        assert isinstance(newdict, OrderedDict) == True
        assert thedict == newdict

    def test_issue_29(self):
        a=[
            ['2016-03-31 10:59', '0123', 'XS360_EU', '04566651561653122'], # error case
            [datetime(2016, 4, 15, 17, 52, 11), 123, False, 456193284757]  #  python types
        ]
        s=pe.get_sheet(array=a)
        content = dedent("""
        Sheet Name: pyexcel_sheet1
        +------------------+------+----------+-------------------+
        | 2016-03-31 10:59 | 0123 | XS360_EU | 04566651561653122 |
        +------------------+------+----------+-------------------+
        | 15/04/16         | 123  | false    | 456193284757      |
        +------------------+------+----------+-------------------+""").strip('\n')
        self.assertEqual(str(s), content)

    def test_issue_29_nominablesheet(self):
        a=[
            ['date', 'number', 'misc', 'long number'],
            ['2016-03-31 10:59', '0123', 'XS360_EU', '04566651561653122'], # error case
            [datetime(2016, 4, 15, 17, 52, 11), 123, False, 456193284757]  #  python types
        ]
        s=pe.get_sheet(array=a)
        s.name_columns_by_row(0)
        content = dedent("""
        Sheet Name: pyexcel_sheet1
        +------------------+--------+----------+-------------------+
        |       date       | number |   misc   |    long number    |
        +==================+========+==========+===================+
        | 2016-03-31 10:59 | 0123   | XS360_EU | 04566651561653122 |
        +------------------+--------+----------+-------------------+
        | 15/04/16         | 123    | false    | 456193284757      |
        +------------------+--------+----------+-------------------+""").strip('\n')
        self.assertEqual(str(s), content)
