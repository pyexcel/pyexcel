"""
    pyexcel.internal.sheets._shared
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Locally shared utility functions

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import re
from pyexcel._compact import PY2


def analyse_slice(aslice, upper_bound):
    """An internal function to analyze a given slice
    """
    if aslice.start is None:
        start = 0
    else:
        start = max(aslice.start, 0)
    if aslice.stop is None:
        stop = upper_bound
    else:
        stop = min(aslice.stop, upper_bound)
    if start > stop:
        raise ValueError
    elif start < stop:
        if aslice.step:
            my_range = range(start, stop, aslice.step)
        else:
            my_range = range(start, stop)
        if not PY2:
            # for py3, my_range is a range object
            my_range = list(my_range)
    else:
        my_range = [start]
    return my_range


def excel_column_index(index_chars):
    if len(index_chars) < 1:
        return -1
    else:
        return _get_index(index_chars.upper())


def excel_cell_position(pos_chars):
    if len(pos_chars) < 2:
        return -1, -1
    group = re.match("([A-Za-z]+)([0-9]+)", pos_chars)
    if group:
        return int(group.group(2)) - 1, excel_column_index(group.group(1))
    else:
        raise IndexError


"""
In order to easily compute the actual index of 'X' or 'AX', these utility
functions were written
"""
_INDICES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _get_index(index_chars):
    length = len(index_chars)
    index_chars_length = len(_INDICES)
    if length > 1:
        index = 0
        for i in range(0, length):
            if i < (length - 1):
                index += ((_INDICES.index(index_chars[i]) + 1) *
                          (index_chars_length ** (length - 1 - i)))
            else:
                index += _INDICES.index(index_chars[i])
        return index
    else:
        return _INDICES.index(index_chars[0])


def names_to_indices(names, series):
    if isinstance(names, str):
        indices = series.index(names)
    elif (isinstance(names, list) and
          isinstance(names[0], str)):
        # translate each row name to index
        indices = [series.index(astr) for astr in names]
    else:
        return names
    return indices
