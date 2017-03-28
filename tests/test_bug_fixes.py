#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from textwrap import dedent

import pyexcel as pe
from datetime import datetime
from _compact import StringIO, OrderedDict
from nose.tools import eq_


def test_bug_01():
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
    assert r[0, 1] == ""
    assert r[3, 1] == ""


def test_issue_03():
    file_prefix = "issue_03_test"
    csv_file = "%s.csv" % file_prefix
    xls_file = "%s.xls" % file_prefix
    my_sheet_name = "mysheetname"
    data = [[1, 1]]
    sheet = pe.Sheet(data, name=my_sheet_name)
    sheet.save_as(csv_file)
    assert(os.path.exists(csv_file))
    sheet.save_as(xls_file)
    book = pe.load_book(xls_file)
    assert book.sheet_names()[0] == my_sheet_name
    os.unlink(csv_file)
    os.unlink(xls_file)


def test_issue_06():
    import logging
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    output = StringIO()
    book = pe.Book({'hoja1': [['datos', 'de', 'prueba'], [1, 2, 3]], })
    book.save_to_memory('csv', output)
    logger.debug(output.getvalue())


def test_issue_09():
    pe.book.LOCAL_UUID = 0
    merged = pe.Book()
    sheet1 = pe.Sheet(sheet=[[1, 2]])
    sheet2 = pe.Sheet(sheet=[[1, 2]])
    merged += sheet1
    merged += sheet2
    eq_(merged[1].name, "pyexcel sheet_1")


def test_issue_10():
    thedict = OrderedDict()
    thedict.update({"Column 1": [1, 2, 3]})
    thedict.update({"Column 2": [1, 2, 3]})
    thedict.update({"Column 3": [1, 2, 3]})
    pe.save_as(adict=thedict, dest_file_name="issue10.xls")
    newdict = pe.get_dict(file_name="issue10.xls")
    assert isinstance(newdict, OrderedDict) is True
    assert thedict == newdict
    os.unlink("issue10.xls")


def test_issue_29():
    a = [
        # error case
        ['2016-03-31 10:59', '0123', 'XS360_EU', '04566651561653122'],
        #  python types
        [datetime(2016, 4, 15, 17, 52, 11), 123, False, 456193284757]
    ]
    s = pe.get_sheet(array=a)
    content = dedent("""
    pyexcel_sheet1:
    +------------------+------+----------+-------------------+
    | 2016-03-31 10:59 | 0123 | XS360_EU | 04566651561653122 |
    +------------------+------+----------+-------------------+
    | 15/04/16         | 123  | false    | 456193284757      |
    +------------------+------+----------+-------------------+""")
    eq_(str(s), content.strip('\n'))


def test_issue_29_nominablesheet():
    a = [
        ['date', 'number', 'misc', 'long number'],
        # error case
        ['2016-03-31 10:59', '0123', 'XS360_EU', '04566651561653122'],
        #  python types
        [datetime(2016, 4, 15, 17, 52, 11), 123, False, 456193284757]
    ]
    s = pe.get_sheet(array=a)
    s.name_columns_by_row(0)
    content = dedent("""
    pyexcel_sheet1:
    +------------------+--------+----------+-------------------+
    |       date       | number |   misc   |    long number    |
    +==================+========+==========+===================+
    | 2016-03-31 10:59 | 0123   | XS360_EU | 04566651561653122 |
    +------------------+--------+----------+-------------------+
    | 15/04/16         | 123    | false    | 456193284757      |
    +------------------+--------+----------+-------------------+""")
    eq_(str(s), content.strip('\n'))


def test_issue_51_orderred_dict_in_records():
    from pyexcel.plugins.sources.pydata import RecordsReader
    records = []
    orderred_dict = OrderedDict()
    orderred_dict.update({"Zebra": 10})
    orderred_dict.update({"Hippo": 9})
    orderred_dict.update({"Monkey": 8})
    records.append(orderred_dict)
    orderred_dict2 = OrderedDict()
    orderred_dict2.update({"Zebra": 1})
    orderred_dict2.update({"Hippo": 2})
    orderred_dict2.update({"Monkey": 3})
    records.append(orderred_dict2)
    records_reader = RecordsReader(records)
    array = list(records_reader.to_array())
    expected = [['Zebra', 'Hippo', 'Monkey'], [10, 9, 8], [1, 2, 3]]
    eq_(array, expected)


def test_issue_51_normal_dict_in_records():
    from pyexcel.plugins.sources.pydata import RecordsReader
    records = []
    orderred_dict = {}
    orderred_dict.update({"Zebra": 10})
    orderred_dict.update({"Hippo": 9})
    orderred_dict.update({"Monkey": 8})
    records.append(orderred_dict)
    orderred_dict2 = {}
    orderred_dict2.update({"Zebra": 1})
    orderred_dict2.update({"Hippo": 2})
    orderred_dict2.update({"Monkey": 3})
    records.append(orderred_dict2)
    records_reader = RecordsReader(records)
    array = list(records_reader.to_array())
    expected = [['Hippo', 'Monkey', 'Zebra'], [9, 8, 10], [2, 3, 1]]
    eq_(array, expected)


def test_issue_55_unicode_in_headers():
    headers = [u'Äkkilähdöt', u'Matkakirjoituksia', u'Matkatoimistot']
    content = [headers, [1, 2, 3]]
    sheet = pe.Sheet(content)
    sheet.name_columns_by_row(0)
    eq_(sheet.colnames, headers)


def test_issue_60_chinese_text_in_python_2_stdout():
    import sys
    data = [['这', '是', '中', '文'], ['这', '是', '中', '文']]
    sheet = pe.Sheet(data)
    sys.stdout.write(repr(sheet))


def test_issue_60_chinese_text_in_python_2_stdout_on_book():
    import sys
    adict = {"Sheet 1": [['这', '是', '中', '文'], ['这', '是', '中', '文']]}
    book = pe.Book()
    book.bookdict = adict
    sys.stdout.write(repr(book))


def test_issue_63_empty_array_crash_texttable_renderer():
    sheet = pe.Sheet([])
    print(sheet)


def test_xls_issue_11():
    data = [[1, 2]]
    sheet = pe.Sheet(data)
    sheet2 = pe.get_sheet(file_content=sheet.xls, file_type='XLS')
    eq_(sheet.array, sheet2.array)
    test_file = 'xls_issue_11.JSON'
    sheet2.save_as(test_file)
    os.unlink(test_file)


def test_issue_68():
    data = [[1]]
    sheet = pe.Sheet(data)
    stream = sheet.save_to_memory('csv')
    eq_(stream.read(), '1\r\n')
    data = {"sheet": [[1]]}
    book = pe.Book(data)
    stream = book.save_to_memory('csv')
    eq_(stream.read(), '1\r\n')


def test_issue_74():
    from decimal import Decimal
    data = [[Decimal("1.1")]]
    sheet = pe.Sheet(data)
    table = sheet.texttable
    expected = 'pyexcel sheet:\n+-----+\n| 1.1 |\n+-----+'
    eq_(table, expected)


def test_issue_76():
    from pyexcel._compact import StringIO
    tsv_stream = StringIO()
    tsv_stream.write('1\t2\t3\t4\n')
    tsv_stream.write('1\t2\t3\t4\n')
    tsv_stream.seek(0)
    sheet = pe.get_sheet(file_stream=tsv_stream, file_type='csv',
                         delimiter='\t')
    data = [
        [1, 2, 3, 4],
        [1, 2, 3, 4]
    ]
    eq_(sheet.array, data)
