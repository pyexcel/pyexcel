"""
pyexcel.cookbook
~~~~~~~~~~~~~~~~~~~

Cookbook for pyexcel

:copyright: (c) 2014-2025 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details
"""

import os

from pyexcel.book import Book
from pyexcel.core import save_as, get_book, get_sheet
from pyexcel._compact import OrderedDict, get_string_file_name
from pyexcel.constants import MESSAGE_WARNING

DEFAULT_OUT_FILE = "pyexcel_merged.csv"
DEFAULT_OUT_XLS_FILE = "merged.xls"
OUT_FILE_FORMATTER = "pyexcel_%s"


def update_columns(in_file_name, column_dicts, out_file_name=None):
    """Update one or more columns of a data file with series

    The data structure of column_dicts should be:
    key should be first row of the column
    the rest of the value should an array
    :param str in_file_name: an accessible file name
    :param dict column_dicts: dictionaries of columns
    :param str out_file_name: save the sheet as


    """
    in_file_name = get_string_file_name(in_file_name)
    default_out_file = OUT_FILE_FORMATTER % in_file_name
    if out_file_name:
        default_out_file = get_string_file_name(out_file_name)
    if os.path.exists(default_out_file):
        raise NotImplementedError(MESSAGE_WARNING)
    sheet = get_sheet(file_name=in_file_name, name_columns_by_row=0)
    series = sheet.colnames
    for k in column_dicts.keys():
        index = series.index(str(k))
        sheet.set_column_at(index, column_dicts[k])
    sheet.save_as(default_out_file)


def update_rows(in_file_name, row_dicts, out_file_name=None):
    """Update one or more rows of a data file with series

    data stucture: key should an integer of the row to be updated
    value should be an array of the data
    :param str in_file_name: an accessible file name
    :param dict row_dicts: dictionaries of rows
    :param str out_file_name: save the sheet as
    """
    in_file_name = get_string_file_name(in_file_name)
    default_out_file = OUT_FILE_FORMATTER % in_file_name
    if out_file_name:
        default_out_file = get_string_file_name(out_file_name)
    if os.path.exists(default_out_file):
        raise NotImplementedError(MESSAGE_WARNING)
    sheet = get_sheet(file_name=in_file_name, name_rows_by_column=0)
    series = sheet.rownames
    for k in row_dicts.keys():
        index = series.index(str(k))
        sheet.set_row_at(index, row_dicts[k])
    sheet.save_as(default_out_file)


def merge_files(file_array, out_file_name=DEFAULT_OUT_FILE):
    """merge many files horizontally column after column
    :param str out_file_name: save the sheet as
    """
    out_file_name = get_string_file_name(out_file_name)
    if os.path.exists(out_file_name):
        raise NotImplementedError(MESSAGE_WARNING)
    content = []
    for file_name in file_array:
        sheet = get_sheet(file_name=file_name)
        content.extend(list(sheet.columns()))
    merged_sheet = get_sheet(array=content)
    merged_sheet.transpose()
    merged_sheet.save_as(out_file_name)
    return out_file_name


def merge_two_files(file1, file2, out_file_name=DEFAULT_OUT_FILE):
    """merge two files

    :param str file1: an accessible file name
    :param str file2: an accessible file name
    :param str out_file_name: save the sheet as
    """
    out_file_name = get_string_file_name(out_file_name)
    if os.path.exists(out_file_name):
        raise NotImplementedError(MESSAGE_WARNING)
    files = [file1, file2]
    merge_files(files, out_file_name)


def merge_readers(reader_array, out_file_name=DEFAULT_OUT_FILE):
    """merge many readers

    With FilterableReader and SeriesReader, you can do custom filtering
    :param str out_file_name: save the sheet as
    """
    out_file_name = get_string_file_name(out_file_name)
    if os.path.exists(out_file_name):
        raise NotImplementedError(MESSAGE_WARNING)
    content = OrderedDict()
    for reader in reader_array:
        content.update(reader.dict)
    save_as(dest_file_name=out_file_name, adict=content)


def merge_two_readers(reader1, reader2, out_file_name=DEFAULT_OUT_FILE):
    """merge two readers

    :param str out_file_name: save the sheet as

    """
    if os.path.exists(out_file_name):
        raise NotImplementedError(MESSAGE_WARNING)
    reader_array = [reader1, reader2]
    merge_readers(reader_array, out_file_name)


def merge_csv_to_a_book(filelist, out_file_name=DEFAULT_OUT_XLS_FILE):
    """merge a list of csv files into a excel book

    :param list filelist: a list of accessible file path
    :param str out_file_name: save the sheet as
    """
    merged = Book()
    for file_name in filelist:
        sheet = get_sheet(file_name=file_name)
        _, tail = os.path.split(file_name)
        sheet.name = tail
        merged += sheet
    merged.save_as(out_file_name)


def merge_all_to_a_book(filelist, out_file_name=DEFAULT_OUT_XLS_FILE):
    """merge a list of excel files into a excel book

    :param list filelist: a list of accessible file path
    :param str out_file_name: save the sheet as
    """
    merged = Book()
    for file_name in filelist:
        merged += get_book(file_name=file_name)
    merged.save_as(out_file_name)


def split_a_book(file_name, out_file_name=None):
    """Split a file into separate sheets

    :param str file_name: an accessible file name
    :param str out_file_name: save the sheets with file suffix
    """
    book = get_book(file_name=file_name)
    if out_file_name:
        saveas = out_file_name
    else:
        saveas = file_name
    for sheet in book:
        filename = f"{sheet.name}_{saveas}"
        sheet.save_as(filename)


def extract_a_sheet_from_a_book(file_name, sheetname, out_file_name=None):
    """Extract a sheet from a excel book

    :param str file_name: an accessible file name
    :param str sheetname: a valid sheet name
    :param str out_file_name: save the sheet as
    """
    book = get_book(file_name=file_name)
    if out_file_name:
        saveas = out_file_name
    else:
        saveas = file_name
    sheet = book[sheetname]
    file_name = f"{sheetname}_{saveas}"
    sheet.save_as(file_name)
