# -*- coding: utf-8 -*-
import os
import pyexcel


class TestCSVUTF:
    def test_write_utf_and_read_back(self):
        data = [
            [u'白', u'日', u'依', u'山', u'尽'],
            [u'黄', u'河', u'入', u'海', u'流'],
            [u'欲', u'穷', u'千', u'里', u'目'],
            [u'更', u'上', u'一', u'层', u'楼']
        ]
        w = pyexcel.Writer("utf.csv")
        w.write_rows(data)
        w.close()
        r = pyexcel.Reader("utf.csv")
        expected = pyexcel.utils.to_array(r)
        print(expected)
        print(data)
        assert expected == data

    def test_csv_book(self):
        b = pyexcel.io.CSVBook(None, None)
        assert b.sheets() == {"csv":[]}

    def tearDown(self):
        if os.path.exists("utf.csv"):
            os.unlink("utf.csv")
