"""
    pyexcel.utils
    ~~~~~~~~~~~~~~~~~~~

    Utility functions for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .sheets import NominableSheet, Sheet
from ._compact import OrderedDict, PY2


def to_array(o):
    """convert a reader iterator to an array"""
    array = []
    for i in o:
        array.append(i)
    return array


def to_dict(o):
    """convert a reader iterator to a dictionary"""
    the_dict = OrderedDict()
    series = "Series_%d"
    count = 1
    for c in o:
        if type(c) == dict:
            the_dict.update(c)
        elif isinstance(c, Sheet):
            the_dict.update({c.name: c.to_array()})
        else:
            key = series % count
            the_dict.update({key: c})
            count += 1
    return the_dict


def to_records(reader, custom_headers=None):
    """
    Make an array of dictionaries

    It takes the first row as keys and the rest of
    the rows as values. Then zips keys and row values
    per each row. This is particularly helpful for
    database operations.
    """
    ret = []
    if isinstance(reader, NominableSheet) is False:
        raise NotImplementedError
    if len(reader.rownames) > 0:
        if custom_headers:
            headers = custom_headers
        else:
            headers = reader.rownames
        for column in reader.columns():
            the_dict = dict(zip(headers, column))
            ret.append(the_dict)
    elif len(reader.colnames) > 0:
        if custom_headers:
            headers = custom_headers
        else:
            headers = reader.colnames
        for row in reader.rows():
            the_dict = dict(zip(headers, row))
            ret.append(the_dict)
    else:
        raise ValueError("No series found")
    return ret


def from_records(records):
    """Reverse function of to_records
    """
    if len(records) < 1:
        return None

    keys = sorted(records[0].keys())
    data = []
    data.append(list(keys))
    for r in records:
        row = []
        for k in keys:
            row.append(r[k])
        data.append(row)
    return data


def to_one_dimensional_array(iterator):
    """convert a reader to one dimensional array"""
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array


def dict_to_array(the_dict, with_keys=True):
    """Convert a dictionary of columns to an array

    The example dict is::

        {
            "Column 1": [1, 2, 3],
            "Column 2": [5, 6, 7, 8],
            "Column 3": [9, 10, 11, 12, 13],
        }

    The output will be::

        [
            ["Column 1", "Column 2", "Column 3"],
            [1, 5, 9],
            [2, 6, 10],
            [3, 7, 11],
            ['', 8, 12],
            ['', '', 13]
        ]

    :param dict the_dict: the dictionary to be converted.
    :param bool with_keys: to write the keys as the first row or not
    """
    content = []
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    if not isinstance(the_dict, OrderedDict):
        keys = sorted(keys)
    if with_keys:
        content.append(keys)
    max_length = -1
    for k in keys:
        column_length = len(the_dict[k])
        if max_length == -1:
            max_length = column_length
        elif max_length < column_length:
            max_length = column_length
    for i in range(0, max_length):
        row_data = []
        for k in keys:
            if i < len(the_dict[k]):
                row_data.append(the_dict[k][i])
            else:
                row_data.append('')
        content.append(row_data)
    return content
