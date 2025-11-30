import os

import pytest
import pyexcel as p

from .base import clean_up_files
from .nose_tools import eq_, raises

content4 = {
    "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
    "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
    "Sheet3": [["X", "Y", "Z"], [1, 4, 7], [2, 5, 8], [3, 6, 9]],
}

content = {
    "X": [1, 2, 3, 4, 5],
    "Y": [6, 7, 8, 9, 10],
    "Z": [11, 12, 13, 14, 15],
}
content2 = {
    "O": [1, 2, 3, 4, 5],
    "P": [6, 7, 8, 9, 10],
    "Q": [11, 12, 13, 14, 15],
}
content3 = {
    "R": [1, 2, 3, 4, 5],
    "S": [6, 7, 8, 9, 10],
    "T": [11, 12, 13, 14, 15],
}


def test_file_1():
    test_file1 = "test1.xls"
    p.save_as(dest_file_name=test_file1, adict=content)
    return test_file1


def test_file_2():
    test_file2 = "test.csv"
    p.save_as(dest_file_name=test_file2, adict=content2)
    return test_file2


def test_file_3():
    test_file3 = "test.xls"
    p.save_as(dest_file_name=test_file3, adict=content3)
    return test_file3


def test_file_0() -> str:
    test_file = "multiple_sheets.xls"
    p.save_book_as(dest_file_name=test_file, bookdict=content4)
    return test_file


def test_split_a_book():
    test_file = test_file_0()
    p.cookbook.split_a_book(test_file, "extracted.csv")
    assert os.path.exists("Sheet1_extracted.csv")
    assert os.path.exists("Sheet2_extracted.csv")
    assert os.path.exists("Sheet3_extracted.csv")
    clean_up_files(
        [
            "Sheet1_extracted.csv",
            "Sheet2_extracted.csv",
            "Sheet3_extracted.csv",
        ]
    )


def test_split_a_book_2():
    """use default output file name"""
    test_file = test_file_0()
    p.cookbook.split_a_book(test_file)
    assert os.path.exists(f"Sheet1_{test_file}")
    assert os.path.exists(f"Sheet2_{test_file}")
    assert os.path.exists(f"Sheet3_{test_file}")
    clean_up_files(
        [f"Sheet1_{test_file}", f"Sheet2_{test_file}", f"Sheet3_{test_file}"]
    )


def test_extract_a_book():
    test_file = test_file_0()
    p.cookbook.extract_a_sheet_from_a_book(
        test_file,
        "Sheet1",
        "extracted.csv",
    )
    assert os.path.exists("Sheet1_extracted.csv")


def test_extract_a_book_2():
    """Use default output file name"""
    test_file = test_file_0()
    p.cookbook.extract_a_sheet_from_a_book(test_file, "Sheet1")
    assert os.path.exists(f"Sheet1_{test_file}")


@raises(ValueError)
def test_update_columns():
    test_file = test_file_0()
    bad_column = {"A": [31, 1, 1, 1, 1]}
    # try non-existent column first
    p.cookbook.update_columns(test_file, bad_column)


@raises(NotImplementedError)
def test_update_columns2():
    test_file = test_file_1()
    custom_column = {"Z": [33, 44, 55, 66, 77]}
    p.cookbook.update_columns(test_file, custom_column)
    r = p.SeriesReader(f"pyexcel_{test_file}")
    data = r.dict
    assert data["Z"] == custom_column["Z"]
    p.cookbook.update_columns(test_file, custom_column, "test4.xls")
    r = p.SeriesReader("test4.xls")
    data = r.dict
    assert data["Z"] == custom_column["Z"]
    # test if it try not overwrite a file
    p.cookbook.update_columns(test_file, custom_column)  # bang


def test_update_rows():
    test_file = test_file_1()
    bad_column = {100: [31, 1, 1, 1, 1]}
    custom_column = {"1": [3, 4]}
    try:
        # try non-existent column first
        p.cookbook.update_rows(test_file, bad_column, out_file_name="a.csv")
        assert 1 == 2
    except ValueError:
        pass
    p.cookbook.update_rows(test_file, custom_column, out_file_name="b.csv")
    r = p.Reader("b.csv")
    assert custom_column["1"] == r.row_at(1)[1:]
    try:
        # try not to overwrite a file
        p.cookbook.update_rows(test_file, custom_column)
        r = p.SeriesReader(f"pyexcel_{test_file}")
        assert 1 == 2
    except NotImplementedError:
        pass
    clean_up_files(["test4.xls"])
    p.cookbook.update_rows(test_file, custom_column, "test4.xls")
    r = p.Reader("test4.xls")
    assert custom_column["1"] == r.row_at(1)[1:]
    clean_up_files(["b.csv"])


@raises(NotImplementedError)
def test_merge_two_files():
    test_file = test_file_1()
    test_file2 = test_file_2()
    p.cookbook.merge_two_files(test_file, test_file2, out_file_name="m.csv")
    r = p.SeriesReader("m.csv")
    r.format(int)
    rcontent = {}
    rcontent.update(content)
    rcontent.update(content2)
    eq_(r.dict, rcontent)
    p.cookbook.merge_two_files(test_file, test_file2)  # bang
    clean_up_files(["m.csv", test_file, test_file2])


def test_merge_files():
    test_file = test_file_1()
    test_file2 = test_file_2()
    test_file3 = test_file_3()
    file_array = [test_file, test_file2, test_file3]
    p.cookbook.merge_files(file_array)
    r = p.SeriesReader("pyexcel_merged.csv")
    r.format(int)
    rcontent = {}
    rcontent.update(content)
    rcontent.update(content2)
    rcontent.update(content3)
    eq_(r.dict, rcontent)
    clean_up_files(["pyexcel_merged.csv", test_file, test_file2])


@raises(NotImplementedError)
def test_merge_two_readers():
    test_file = test_file_1()
    test_file2 = test_file_2()
    r1 = p.SeriesReader(test_file)
    r2 = p.SeriesReader(test_file2)
    p.cookbook.merge_two_readers(r1, r2)
    r = p.SeriesReader("pyexcel_merged.csv")
    r.format(int)
    rcontent = {}
    rcontent.update(content)
    rcontent.update(content2)
    eq_(r.dict, rcontent)
    p.cookbook.merge_two_readers(r1, r2)  # bang, do not overwrite
    clean_up_files(["pyexcel_merged.csv", test_file, test_file2])


@raises(NotImplementedError)
def test_merge_readers():
    test_file = test_file_1()
    test_file2 = test_file_2()
    test_file3 = test_file_3()
    r1 = p.SeriesReader(test_file)
    r2 = p.SeriesReader(test_file2)
    r3 = p.SeriesReader(test_file3)
    file_array = [r1, r2, r3]
    p.cookbook.merge_readers(file_array)
    r = p.SeriesReader("pyexcel_merged.csv")
    r.format(int)
    content = {}
    content.update(content)
    content.update(content2)
    content.update(content3)
    eq_(r.dict, content)
    p.cookbook.merge_readers(file_array)  # bang, do not overwrite


def test_merge_any_files_to_a_book():
    test_file1 = test_file_1()
    test_file2 = test_file_2()
    test_file3 = test_file_3()
    test_file0 = test_file_0()
    file_array = [
        test_file1,
        test_file2,
        test_file3,
        test_file0,
    ]
    p.cookbook.merge_all_to_a_book(file_array, "merged.xlsx")
    r = p.BookReader("merged.xlsx")
    r[test_file1].name_columns_by_row(0)
    rcontent = r[test_file1].to_dict()
    assert rcontent == content
    r[test_file2].format(int)
    r[test_file2].name_columns_by_row(0)
    rcontent2 = r[test_file2].to_dict()
    assert rcontent2 == content2
    r[test_file3].name_columns_by_row(0)
    rcontent3 = r[test_file3].to_dict()
    assert rcontent3 == content3
    rcontent4 = r["Sheet1"].to_array()
    assert rcontent4 == content4["Sheet1"]
    rcontent5 = r["Sheet2"].to_array()
    assert rcontent5 == content4["Sheet2"]
    rcontent6 = r["Sheet3"].to_array()
    assert rcontent6 == content4["Sheet3"]


def test_merge_csv_files_to_a_book():
    test_file = test_file_1()
    test_file2 = test_file_2()
    test_file3 = test_file_3()
    file_array = [test_file, test_file2, test_file3]
    p.cookbook.merge_csv_to_a_book(file_array, "merged.xlsx")
    r = p.BookReader("merged.xlsx")
    r[test_file].name_columns_by_row(0)
    content = r[test_file].to_dict()
    assert content == content
    r[test_file2].format(int)
    r[test_file2].name_columns_by_row(0)
    content2 = r[test_file2].to_dict()
    assert content2 == content2
    r[test_file3].name_columns_by_row(0)
    content3 = r[test_file3].to_dict()
    assert content3 == content3


def test_clean_up_files():
    file_list = [
        test_file_0(),
        test_file_1(),
        test_file_2(),
        test_file_3(),
        "pyexcel_merged.csv",
        "merged.xlsx",
        "merged.xls",
        "test4.xls",
        "Sheet1_extracted.csv",
        "Sheet2_extracted.csv",
        "Sheet3_extracted.csv",
        "Sheet1_multiple_sheets.xls",
        "Sheet2_multiple_sheets.xls",
        "Sheet3_multiple_sheets.xls",
    ]
    clean_up_files(file_list)
