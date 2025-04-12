#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from textwrap import dedent

import psutil
import pyexcel as p

from nose.tools import eq_
from ._compact import StringIO, OrderedDict


def test_bug_01():
    """
    if first row of csv is shorter than the rest of the rows,
    the csv will be truncated by first row. This is a bug

    "a,d,e,f" <- this will be 1
    '1',2,3,4 <- 4
    '2',3,4,5
    'b'       <- give '' for missing cells
    """
    r = p.Reader(os.path.join("tests", "fixtures", "bug_01.csv"))
    assert len(r.row[0]) == 4
    # test "" is append for empty cells
    assert r[0, 1] == ""
    assert r[3, 1] == ""


def test_issue_03():
    file_prefix = "issue_03_test"
    csv_file = f"{file_prefix}.csv"
    xls_file = f"{file_prefix}.xls"
    my_sheet_name = "mysheetname"
    data = [[1, 1]]
    sheet = p.Sheet(data, name=my_sheet_name)
    sheet.save_as(csv_file)
    assert os.path.exists(csv_file)
    sheet.save_as(xls_file)
    book = p.load_book(xls_file)
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
    book = p.Book({"hoja1": [["datos", "de", "prueba"], [1, 2, 3]]})
    book.save_to_memory("csv", output)
    logger.debug(output.getvalue())


def test_issue_09():
    p.book.LOCAL_UUID = 0
    merged = p.Book()
    sheet1 = p.Sheet(sheet=[[1, 2]])
    sheet2 = p.Sheet(sheet=[[1, 2]])
    merged += sheet1
    merged += sheet2
    eq_(merged[1].name, "pyexcel sheet_1")


def test_issue_10():
    thedict = OrderedDict()
    thedict.update({"Column 1": [1, 2, 3]})
    thedict.update({"Column 2": [1, 2, 3]})
    thedict.update({"Column 3": [1, 2, 3]})
    p.save_as(adict=thedict, dest_file_name="issue10.xls")
    newdict = p.get_dict(file_name="issue10.xls")
    assert isinstance(newdict, OrderedDict) is True
    eq_(thedict, newdict)
    os.unlink("issue10.xls")


def test_issue_29():
    a = [
        # error case
        ["2016-03-31 10:59", "0123", "XS360_EU", "04566651561653122"],
        #  python types
        [datetime(2016, 4, 15, 17, 52, 11), 123, False, 456193284757],
    ]
    s = p.get_sheet(array=a)
    content = dedent(
        """
    pyexcel_sheet1:
    +------------------+------+----------+-------------------+
    | 2016-03-31 10:59 | 0123 | XS360_EU | 04566651561653122 |
    +------------------+------+----------+-------------------+
    | 15/04/16         | 123  | false    | 456193284757      |
    +------------------+------+----------+-------------------+""",
    )
    eq_(str(s), content.strip("\n"))


def test_issue_29_nominablesheet():
    a = [
        ["date", "number", "misc", "long number"],
        # error case
        ["2016-03-31 10:59", "0123", "XS360_EU", "04566651561653122"],
        #  python types
        [datetime(2016, 4, 15, 17, 52, 11), 123, False, 456193284757],
    ]
    s = p.get_sheet(array=a)
    s.name_columns_by_row(0)
    content = dedent(
        """
    pyexcel_sheet1:
    +------------------+--------+----------+-------------------+
    |       date       | number |   misc   |    long number    |
    +==================+========+==========+===================+
    | 2016-03-31 10:59 | 0123   | XS360_EU | 04566651561653122 |
    +------------------+--------+----------+-------------------+
    | 15/04/16         | 123    | false    | 456193284757      |
    +------------------+--------+----------+-------------------+""",
    )
    eq_(str(s), content.strip("\n"))


def test_issue_51_orderred_dict_in_records():
    from pyexcel.plugins.sources.pydata.records import RecordsReader

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
    expected = [["Zebra", "Hippo", "Monkey"], [10, 9, 8], [1, 2, 3]]
    eq_(array, expected)


def test_issue_51_normal_dict_in_records():
    from pyexcel.plugins.sources.pydata.records import RecordsReader

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
    expected = [["Hippo", "Monkey", "Zebra"], [9, 8, 10], [2, 3, 1]]
    eq_(array, expected)


def test_issue_55_unicode_in_headers():
    headers = ["Äkkilähdöt", "Matkakirjoituksia", "Matkatoimistot"]
    content = [headers, [1, 2, 3]]
    sheet = p.Sheet(content)
    sheet.name_columns_by_row(0)
    eq_(sheet.colnames, headers)


def test_issue_60_chinese_text_in_python_2_stdout():
    import sys

    data = [["这", "是", "中", "文"], ["这", "是", "中", "文"]]
    sheet = p.Sheet(data)
    sys.stdout.write(repr(sheet))


def test_issue_60_chinese_text_in_python_2_stdout_on_book():
    import sys

    adict = {"Sheet 1": [["这", "是", "中", "文"], ["这", "是", "中", "文"]]}
    book = p.Book()
    book.bookdict = adict
    sys.stdout.write(repr(book))


def test_issue_63_empty_array_crash_texttable_renderer():
    sheet = p.Sheet([])
    print(sheet)


def test_xls_issue_11():
    data = [[1, 2]]
    sheet = p.Sheet(data)
    sheet2 = p.get_sheet(file_content=sheet.xls, file_type="XLS")
    eq_(sheet.array, sheet2.array)
    test_file = "xls_issue_11.JSON"
    sheet2.save_as(test_file)
    os.unlink(test_file)


def test_issue_68():
    data = [[1]]
    sheet = p.Sheet(data)
    stream = sheet.save_to_memory("csv")
    eq_(stream.read(), "1\r\n")
    data = {"sheet": [[1]]}
    book = p.Book(data)
    stream = book.save_to_memory("csv")
    eq_(stream.read(), "1\r\n")


def test_issue_74():
    from decimal import Decimal

    data = [[Decimal("1.1")]]
    sheet = p.Sheet(data)
    table = sheet.texttable
    expected = "pyexcel sheet:\n+-----+\n| 1.1 |\n+-----+"
    eq_(table, expected)


def test_issue_76():
    from pyexcel._compact import StringIO

    tsv_stream = StringIO()
    tsv_stream.write("1\t2\t3\t4\n")
    tsv_stream.write("1\t2\t3\t4\n")
    tsv_stream.seek(0)
    sheet = p.get_sheet(
        file_stream=tsv_stream,
        file_type="csv",
        delimiter="\t",
    )
    data = [[1, 2, 3, 4], [1, 2, 3, 4]]
    eq_(sheet.array, data)


def test_issue_83_csv_file_handle():
    proc = psutil.Process()
    test_file = os.path.join("tests", "fixtures", "bug_01.csv")
    open_files_l1 = proc.open_files()

    # start with a csv file
    data = p.iget_array(file_name=test_file)
    open_files_l2 = proc.open_files()
    delta = len(open_files_l2) - len(open_files_l1)
    # interestingly, no open file handle yet
    assert delta == 0

    # now the file handle get opened when we run through
    # the generator
    list(data)
    open_files_l3 = proc.open_files()
    delta = len(open_files_l3) - len(open_files_l1)
    # caught an open file handle, the "fish" finally
    assert delta == 1

    # free the fish
    p.free_resources()
    open_files_l4 = proc.open_files()
    # this confirms that no more open file handle
    eq_(open_files_l1, open_files_l4)


def test_issue_83_file_handle_no_generator():
    proc = psutil.Process()
    test_files = [
        os.path.join("tests", "fixtures", "bug_01.csv"),
        os.path.join("tests", "fixtures", "test-single.csvz"),
        os.path.join("tests", "fixtures", "date_field.xls"),
    ]
    for test_file in test_files:
        open_files_l1 = proc.open_files()
        # start with a csv file
        p.get_array(file_name=test_file)
        open_files_l2 = proc.open_files()
        delta = len(open_files_l2) - len(open_files_l1)
        # no open file handle should be left
        assert delta == 0


def test_issue_83_csvz_file_handle():
    proc = psutil.Process()
    test_file = os.path.join("tests", "fixtures", "test-single.csvz")
    open_files_l1 = proc.open_files()

    # start with a csv file
    data = p.iget_array(file_name=test_file)
    open_files_l2 = proc.open_files()
    delta = len(open_files_l2) - len(open_files_l1)
    # interestingly, file is already open :)
    assert delta == 1

    # now the file handle get opened when we run through
    # the generator
    list(data)
    open_files_l3 = proc.open_files()
    delta = len(open_files_l3) - len(open_files_l1)
    # caught an open file handle, the "fish" finally
    assert delta == 1

    # free the fish
    p.free_resources()
    open_files_l4 = proc.open_files()
    # this confirms that no more open file handle
    eq_(open_files_l1, open_files_l4)


def test_issue_83_xls_file_handle():
    proc = psutil.Process()
    test_file = os.path.join("tests", "fixtures", "date_field.xls")
    open_files_l1 = proc.open_files()

    # start with a csv file
    data = p.iget_array(file_name=test_file)
    open_files_l2 = proc.open_files()
    delta = len(open_files_l2) - len(open_files_l1)
    # interestingly, no open file using xlrd
    assert delta == 0

    # now the file handle get opened when we run through
    # the generator
    list(data)
    open_files_l3 = proc.open_files()
    delta = len(open_files_l3) - len(open_files_l1)
    # still no open file
    assert delta == 0

    p.free_resources()
    open_files_l4 = proc.open_files()
    eq_(open_files_l1, open_files_l4)


def test_issue_92_non_uniform_records():
    records = [{"a": 1}, {"b": 2}, {"c": 3}]
    sheet = p.get_sheet(records=records, custom_headers=["a", "b", "c"])
    content = dedent(
        """
    +---+---+---+
    | a | b | c |
    +---+---+---+
    | 1 |   |   |
    +---+---+---+
    |   | 2 |   |
    +---+---+---+
    |   |   | 3 |
    +---+---+---+""",
    ).strip("\n")
    eq_(str(sheet.content), content)


def test_issue_92_incomplete_records():
    records = [{"a": 1, "b": 2, "c": 3}, {"b": 2}, {"c": 3}]
    sheet = p.get_sheet(records=records)
    content = dedent(
        """
    +---+---+---+
    | a | b | c |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    |   | 2 |   |
    +---+---+---+
    |   |   | 3 |
    +---+---+---+""",
    ).strip("\n")
    eq_(str(sheet.content), content)


def test_issue_92_verify_save_as():
    records = [{"a": 1, "b": 2, "c": 3}, {"b": 2}, {"c": 3}]
    csv_io = p.save_as(records=records, dest_file_type="csv")
    content = "a,b,c\r\n1,2,3\r\n,2,\r\n,,3\r\n"
    eq_(csv_io.getvalue(), content)


def test_issue_95_preserve_order_in_iget_orders():
    test_data = [["a", "b", "c"], ["1", "2", "3"], ["4", "5", "6"]]

    records = p.iget_records(array=test_data)
    result = []
    for record in records:
        for key, value in record.items():
            result.append([key, value])

    expected = [
        ["a", "1"],
        ["b", "2"],
        ["c", "3"],
        ["a", "4"],
        ["b", "5"],
        ["c", "6"],
    ]
    eq_(result, expected)


def test_issue_95_preserve_custom_order_in_iget_orders():
    test_data = [["a", "b", "c"], ["1", "2", "3"], ["4", "5", "6"]]

    records = p.iget_records(array=test_data, custom_headers=["c", "a", "b"])
    result = []
    for record in records:
        for key, value in record.items():
            result.append([key, value])

    expected = [
        ["c", "3"],
        ["a", "1"],
        ["b", "2"],
        ["c", "6"],
        ["a", "4"],
        ["b", "5"],
    ]
    eq_(result, expected)


def test_issue_95_preserve_order_in_get_orders():
    test_data = [["a", "b", "c"], ["1", "2", "3"], ["4", "5", "6"]]

    records = p.get_records(array=test_data)
    result = []
    for record in records:
        for key, value in record.items():
            result.append([key, value])

    expected = [
        ["a", "1"],
        ["b", "2"],
        ["c", "3"],
        ["a", "4"],
        ["b", "5"],
        ["c", "6"],
    ]
    eq_(result, expected)


def test_issue_100():
    data = [["a", "b"]]
    sheet = p.Sheet(data)
    sheet.name_columns_by_row(0)
    eq_(sheet.to_dict(), {"a": [], "b": []})


def test_issue_125():
    book = p.Book()
    book += p.Sheet([[1]], "A")
    book += p.Sheet([[2]], "B")
    eq_(book.sheet_names(), ["A", "B"])
    book.sort_sheets(reverse=True)
    eq_(book.sheet_names(), ["B", "A"])


def test_issue_125_saving_the_order():
    test_file = "issue_125.xls"
    book = p.Book()
    book += p.Sheet([[1]], "A")
    book += p.Sheet([[2]], "B")
    eq_(book.sheet_names(), ["A", "B"])
    book.sort_sheets(reverse=True)
    book.save_as(test_file)
    book2 = p.get_book(file_name=test_file)
    eq_(book2.sheet_names(), ["B", "A"])
    os.unlink(test_file)


def test_issue_125_using_key():
    test_file = "issue_125.xls"
    book = p.Book()
    book += p.Sheet([[1]], "A")
    book += p.Sheet([[2]], "B")
    book += p.Sheet([[3]], "C")

    custom_order = {"A": 1, "B": 3, "C": 2}
    book.sort_sheets(key=lambda x: custom_order[x])
    book.save_as(test_file)
    book2 = p.get_book(file_name=test_file)
    eq_(book2.sheet_names(), ["A", "C", "B"])
    os.unlink(test_file)


def test_issue_126():
    data = [[1]]
    test_file = "issue_126.xls"
    test_name = "doyoufindme"
    p.save_as(array=data, dest_file_name=test_file, dest_sheet_name=test_name)
    sheet = p.get_sheet(file_name=test_file)
    eq_(sheet.name, test_name)
    os.unlink(test_file)


def test_issue_126_isave_as():
    data = [[1]]
    test_file = "issue_126.xls"
    test_name = "doyoufindme"
    p.isave_as(array=data, dest_file_name=test_file, dest_sheet_name=test_name)
    sheet = p.get_sheet(file_name=test_file)
    eq_(sheet.name, test_name)
    os.unlink(test_file)


def test_pyexcel_issue_138():
    sheet = p.Sheet()
    sheet.csv = "123_122,"
    eq_(sheet[0, 0], "123_122")


def test_pyexcel_issue_140():
    TestSheet1 = p.Sheet()
    TestSheet1[4, 4] = "4x4"
    TestSheet1[0, 0] = "0,0"
    expected = [
        ["0,0", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", "4x4"],
    ]
    eq_(expected, TestSheet1.to_array())


def test_pyexcel_issue_176():
    sheet = p.get_sheet(
        file_name=os.path.join("tests", "fixtures", "bug_176.xlsx"),
    )
    eq_("<No data>", sheet.name)
    eq_([[]], sheet.array)


def test_pyexcel_issue_176_get_book():
    book = p.get_book(
        file_name=os.path.join("tests", "fixtures", "bug_176.xlsx"),
    )
    eq_({}, book.bookdict)


def test_issue_241():
    import glob

    from pyexcel import get_book, merge_all_to_a_book

    merge_all_to_a_book(
        glob.glob("tests/fixtures/issue_241/*.csv"),
        "issue_241.xlsx",
    )
    book = get_book(file_name="issue_241.xlsx")
    book.sort_sheets()
    expected = dedent(
        """
    1.csv:
    +---------+---+---------+---------+
    | header1 |   | header3 | header4 |
    +---------+---+---------+---------+
    | 1       | 2 | 3       | 4       |
    +---------+---+---------+---------+
    2.csv:
    +---------+---------+---+---------+
    | headerA | headerB |   | headerD |
    +---------+---------+---+---------+
    | A       |         | C | D       |
    +---------+---------+---+---------+
    | F       | G       | M | T       |
    +---------+---------+---+---------+""",
    ).lstrip()
    eq_(str(book), expected)
    os.unlink("issue_241.xlsx")


def test_issue_250():
    from copy import deepcopy

    s = p.Sheet()
    deepcopy(s)
