"""
    pyexcel.cookbook
    ~~~~~~~~~~~~~~~~~~~

    Cookbook for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import os
from readers import SeriesReader, Reader, BookReader
from utils import to_dict, to_array
from writers import Writer, BookWriter


__WARNING_TEXT__ = "We do not overwrite files"


def update_columns(infilename, column_dicts, outfilename=None):
    """Update one or more columns of a data file with series

    The data structure of column_dicts should be:
    key should be first row of the column
    the rest of the value should an array
    """
    default_out_file = "pyexcel_%s" % infilename
    if outfilename:
        default_out_file = outfilename
    if os.path.exists(default_out_file):
        raise NotImplementedError(__WARNING_TEXT__)
    r = SeriesReader(infilename)
    series = r.series()
    for k in column_dicts.keys():
        index = series.index(k)
        r.set_column_at(index, column_dicts[k])
    w = Writer(default_out_file)
    w.write_reader(r)
    w.close()


def update_rows(infilename, row_dicts, outfilename=None):
    """Update one or more columns of a data file with series

    datastucture: key should an integer of the row to be updated
    value should be an array of the data
    """
    default_out_file = "pyexcel_%s" % infilename
    if outfilename:
        default_out_file = outfilename
    if os.path.exists(default_out_file):
        raise NotImplementedError(__WARNING_TEXT__)
    r = Reader(infilename)
    for k in row_dicts.keys():
        r.set_row_at(k, row_dicts[k])
    w = Writer(default_out_file)
    w.write_reader(r)
    w.close()


def merge_files(file_array, outfilename="pyexcel_merged.csv"):
    """merge many files horizontally column after column"""
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
    """merge two files"""
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    files = [file1, file2]
    merge_files(files, outfilename)


def merge_readers(reader_array, outfilename="pyexcel_merged.csv"):
    """merge many readers

    With FilterableReader and SeriesReader, you can do custom filtering
    """
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    content = {}
    for r in reader_array:
        content.update(to_dict(r))
    w = Writer(outfilename)
    w.write_dict(content)
    w.close()


def merge_two_readers(reader1, reader2, outfilename="pyexcel_merged.csv"):
    """merge two readers"""
    if os.path.exists(outfilename):
        raise NotImplementedError(__WARNING_TEXT__)
    reader_array = [reader1, reader2]
    merge_readers(reader_array, outfilename)


def merge_csv_to_a_book(filelist, outfilename="merged.xls"):
    """merge a list of csv files into a excel book"""
    w = BookWriter(outfilename)
    for file in filelist:
        r = Reader(file)
        head, tail = os.path.split(file)
        sheet = w.create_sheet(tail)
        sheet.write_reader(r)
        sheet.close()
    w.close()


def merge_all_to_a_book(filelist, outfilename="merged.xls"):
    """merge a list of csv files into a excel book

    Note: empty sheets are ignored
    """
    w = BookWriter(outfilename)
    for file in filelist:
        r = BookReader(file)
        head, tail = os.path.split(file)
        count = 0
        # find out if the file is a single sheet book
        # or a multiple sheet book
        for sheet in r:
            if sheet.number_of_rows() > 0:
                count += 1

        for sheet in r:
            if sheet.number_of_rows() > 0:
                if count == 1:
                    # single sheet book, just use the file name
                    # for the sheet name
                    sheet_name = tail
                else:
                    # otherwise: filename_sheetname
                    sheet_name = "%s_%s" % (tail, sheet.name)
                new_sheet = w.create_sheet(sheet_name)
                new_sheet.write_reader(sheet)
                new_sheet.close()
    w.close()


def split_a_book(file, outfilename=None):
    """Split a file into separate sheets"""
    r = BookReader(file)
    if outfilename:
        saveas = outfilename
    else:
        saveas = file
    for sheet in r:
        w = Writer("%s_%s" % (sheet.name, saveas))
        w.write_reader(sheet)
        w.close()


def extract_a_sheet_from_a_book(file, sheetname, outfilename=None):
    """Extract a sheet from a excel book"""
    r = BookReader(file)
    if outfilename:
        saveas = outfilename
    else:
        saveas = file
    sheet = r[sheetname]
    w = Writer("%s_%s" % (sheetname, saveas))
    w.write_reader(sheet)
    w.close()


class SHEET:
    def __init__(self, file):
        self.file = file

    def __add__(self, other):
        return merge_files([self.file, other.file])
