"""
    pyexcel.cookbook
    ~~~~~~~~~~~~~~~~~~~

    Cookbook for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import os
from .book import Book, load_book
from .sheets import load, Reader
from .utils import to_dict, to_array
from .writers import Writer, BookWriter
from ._compact import OrderedDict


__WARNING_TEXT__ = "We do not overwrite files"


def update_columns(infilename, column_dicts, outfilename=None):
    """Update one or more columns of a data file with series

    The data structure of column_dicts should be:
    key should be first row of the column
    the rest of the value should an array
    :param str infilename: an accessible file name
    :param dict column_dicts: dictionaries of columns
    :param str outfilename: save the sheet as


    """
    default_out_file = "pyexcel_%s" % infilename
    if outfilename:
        default_out_file = outfilename
    if os.path.exists(default_out_file):
        raise NotImplementedError(__WARNING_TEXT__)
    r = load(infilename, name_columns_by_row=0)
    series = r.colnames
    for k in column_dicts.keys():
        index = series.index(str(k))
        r.set_column_at(index, column_dicts[k])
    w = Writer(default_out_file)
    w.write_reader(r)
    w.close()


def update_rows(infilename, row_dicts, outfilename=None):
    """Update one or more columns of a data file with series

    datastucture: key should an integer of the row to be updated
    value should be an array of the data
    :param str infilename: an accessible file name
    :param dict row_dicts: dictionaries of rows
    :param str outfilename: save the sheet as
    """
    default_out_file = "pyexcel_%s" % infilename
    if outfilename:
        default_out_file = outfilename
    if os.path.exists(default_out_file):
        raise NotImplementedError(__WARNING_TEXT__)
    r = load(infilename, name_rows_by_column=0)
    series = r.rownames
    for k in row_dicts.keys():
        index = series.index(str(k))
        r.set_row_at(index, row_dicts[k])
    r.save_as(default_out_file)


def merge_files(file_array, outfilename="pyexcel_merged.csv"):
    """merge many files horizontally column after column
    :param str outfilename: save the sheet as
    """
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    content = []
    for f in file_array:
        r = Reader(f)
        content.extend(to_array(r.columns()))
    w = Writer(outfilename)
    w.write_columns(content)
    w.close()
    return outfilename


def merge_two_files(file1, file2, outfilename="pyexcel_merged.csv"):
    """merge two files
    
    :param str file1: an accessible file name
    :param str file2: an accessible file name
    :param str outfilename: save the sheet as
    """
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    files = [file1, file2]
    merge_files(files, outfilename)


def merge_readers(reader_array, outfilename="pyexcel_merged.csv"):
    """merge many readers

    With FilterableReader and SeriesReader, you can do custom filtering
    :param str outfilename: save the sheet as
    """
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    content = OrderedDict()
    for r in reader_array:
        content.update(to_dict(r))
    w = Writer(outfilename)
    w.write_dict(content)
    w.close()


def merge_two_readers(reader1, reader2, outfilename="pyexcel_merged.csv"):
    """merge two readers

    :param str outfilename: save the sheet as

    """
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    reader_array = [reader1, reader2]
    merge_readers(reader_array, outfilename)


def merge_csv_to_a_book(filelist, outfilename="merged.xls"):
    """merge a list of csv files into a excel book

    :param list filelist: a list of accessible file path
    :param str outfilename: save the sheet as
    """
    w = BookWriter(outfilename)
    for file in filelist:
        r = Reader(file)
        head, tail = os.path.split(file)
        sheet = w.create_sheet(tail)
        sheet.write_reader(r)
        sheet.close()
    w.close()


def merge_all_to_a_book(filelist, outfilename="merged.xls"):
    """merge a list of excel files into a excel book

    :param list filelist: a list of accessible file path
    :param str outfilename: save the sheet as
    """
    merged = Book()
    for file in filelist:
        merged += load_book(file)
    w = BookWriter(outfilename)
    w.write_book_reader(merged)
    w.close()


def split_a_book(file, outfilename=None):
    """Split a file into separate sheets
    
    :param str file: an accessible file name
    :param str outfilename: save the sheets with file suffix
    """
    r = load_book(file)
    if outfilename:
        saveas = outfilename
    else:
        saveas = file
    for sheet in r:
        w = Writer("%s_%s" % (sheet.name, saveas))
        w.write_reader(sheet)
        w.close()


def extract_a_sheet_from_a_book(file, sheetname, outfilename=None):
    """Extract a sheet from a excel book

    :param str file: an accessible file
    :param str sheetname: a valid sheet name
    :param str outfilename: save the sheet as
    """
    r = load_book(file)
    if outfilename:
        saveas = outfilename
    else:
        saveas = file
    sheet = r[sheetname]
    w = Writer("%s_%s" % (sheetname, saveas))
    w.write_reader(sheet)
    w.close()
