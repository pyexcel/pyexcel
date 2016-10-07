"""
    pyexcel.utils
    ~~~~~~~~~~~~~~~~~~~

    Utility functions for pyexcel

    :copyright: (c) 2014-2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel.sheets import Sheet
from pyexcel._compact import OrderedDict, PY2
from pyexcel._compact import zip_longest


LOCAL_UUID = 0


def local_uuid():
    global LOCAL_UUID
    LOCAL_UUID = LOCAL_UUID + 1
    return LOCAL_UUID


def xto_dict(an_object):
    """convert a reader iterator to a dictionary"""
    the_dict = OrderedDict()
    series = "Series_%d"
    count = 1
    for row in an_object:
        if type(row) == dict:
            the_dict.update(row)
        elif isinstance(row, Sheet):
            the_dict.update({row.name: row.to_array()})
        else:
            key = series % count
            the_dict.update({key: row})
            count += 1
    return the_dict


def yield_from_records(records):
    """Reverse function of to_records
    """
    if len(records) < 1:
        yield []
    else:
        first_record = records[0]
        if isinstance(first_record, OrderedDict):
            keys = first_record.keys()
        else:
            keys = sorted(first_record.keys())
        yield list(keys)
        for r in records:
            row = []
            for k in keys:
                row.append(r[k])
            yield row


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
    sorted_values = (the_dict[key] for key in keys)
    for row in zip_longest(*sorted_values, fillvalue=''):
        yield list(row)


def convert_dict_to_ordered_dict(the_dict):
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    keys = sorted(keys)
    ret = OrderedDict()
    for key in keys:
        ret[key] = the_dict[key]
    return ret
