"""
    pyexcel.utils
    ~~~~~~~~~~~~~~~~~~~

    Utility functions for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""

from .common import Sheet
from .readers import load_file
import json


def jsonify(filename):
    """
    Get the excel data in json
    """
    book = load_file(filename)
    return json.dumps(book.sheets)


def to_array(o):
    """convert a reader iterator to an array"""
    array = []
    if isinstance(o, str):
        book = load_file(file)
        sheet_names = book.sheets.keys()
        if len(sheet_names) == 1:
            array = book.sheets[sheet_names[0]]
        else:
            array.append(sheet_names)
            for name in sheet_names:
                array.append(book.sheets[name])
    else:
        for i in o:
            array.append(i)
    return array


def to_dict(o):
    """convert a reader iterator to a dictionary"""
    the_dict = {}
    if isinstance(o, str):
        book = load_file(o)
        the_dict = book.sheets
    else:
        series = "Series_%d"
        count = 1
        for c in o:
            if type(c) == dict:
                the_dict.update(c)
            elif isinstance(c, Sheet):
                the_dict.update({c.name: to_array(c)})
            else:
                key = series % count
                the_dict.update({key: c})
                count += 1
    return the_dict


def to_records(reader):
    """
    Make an array of dictionaries

    It takes the first row as keys and the rest of
    the rows as values. Then zips keys and row values
    per each row. This is particularly helpful for
    database operations.
    """
    if isinstance(reader, Sheet) is False:
        raise NotImplementedError
    headers = reader.series()
    need_revert = False
    if len(headers) == 0:
        reader.become_series()
        headers = reader.series()
        need_revert = True
    ret = []
    for row in reader.rows():
        the_dict = dict(zip(headers, row))
        ret.append(the_dict)

    if need_revert:
        reader.become_sheet()
    return ret


def to_one_dimensional_array(iterator):
    """convert a reader to one dimensional array"""
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array
