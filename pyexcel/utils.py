"""
    pyexcel.utils
    ~~~~~~~~~~~~~~~~~~~

    Utility functions for pyexcel

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .sheets import NominableSheet, Sheet
from ._compact import OrderedDict, PY2
from .constants import MESSAGE_DATA_ERROR_NO_SERIES
from functools import partial
from ._compact import deprecated
import datetime


LOCAL_UUID = 0

def local_uuid():
    global LOCAL_UUID
    LOCAL_UUID = LOCAL_UUID + 1
    return LOCAL_UUID


deprecated_utls = partial(deprecated,
                          message="Deprecated since v0.2.0!")


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
        raise ValueError(MESSAGE_DATA_ERROR_NO_SERIES)
    return ret


@deprecated_utls
def from_records(records):
    """Reverse function of to_records
    """
    content = list(yield_from_records(records))
    if content == [[]]:
        return None
    else:
        return content

    
def yield_from_records(records):
    """Reverse function of to_records
    """
    if len(records) < 1:
        yield []
    else:
        keys = sorted(records[0].keys())
        yield list(keys)
        for r in records:
            row = []
            for k in keys:
                row.append(r[k])
            yield row


def to_one_dimensional_array(iterator):
    """convert a reader to one dimensional array"""
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array


@deprecated_utls
def dict_to_array(the_dict, with_keys=True):
    return list(yield_dict_to_array(the_dict, with_keys))


def yield_dict_to_array(the_dict, with_keys=True):
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
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    if not isinstance(the_dict, OrderedDict):
        keys = sorted(keys)
    if with_keys:
        yield keys
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
        yield row_data


def from_query_sets(column_names, query_sets):
    array = []
    array.append(column_names)
    for o in query_sets:
        new_array = []
        for column in column_names:
            value = getattr(o, column)
            if isinstance(value, (datetime.date, datetime.time)):
                value = value.isoformat()
            new_array.append(value)
        array.append(new_array)
    return array


def convert_dict_to_ordered_dict(the_dict):
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    keys = sorted(keys)
    ret = OrderedDict()
    for key in keys:
        ret[key] = the_dict[key]
    return ret
