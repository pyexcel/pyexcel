"""
    pyexcel.internal.sheets._shared
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Locally shared utility functions

    :copyright: (c) 2015-2022 by Onni Software Ltd.
    :license: New BSD License
"""
import re
import types
from typing import Tuple
from functools import partial

from pyexcel._compact import PY2

from .formatters import to_format


class CommonPropertyAmongRowNColumn(object):
    """
    Group reusable functions from row and column
    """

    def __init__(self, matrix):
        self._ref = matrix

    def __iadd__(self, other):
        raise NotImplementedError("Not implemented")

    def __add__(self, other):
        """Overload + sign

        :return: self
        """
        self.__iadd__(other)
        return self._ref

    @staticmethod
    def get_converter(theformatter):
        """return the actual converter or a built-in converter"""
        converter = None
        if isinstance(theformatter, types.FunctionType):
            converter = theformatter
        else:
            converter = partial(to_format, theformatter)
        return converter


def analyse_slice(aslice, upper_bound):
    """An internal function to analyze a given slice"""
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


def excel_cell_position(pos_chars: str) -> Tuple[int, int]:
    """
    translate MS excel position to index
    Return: (row: int, column: int)
    """
    match = re.match("([A-Za-z]+)([0-9]+)", pos_chars)

    if match:
        return int(match.group(2)) - 1, excel_column_index(match.group(1))
    else:
        raise IndexError(f"invalid index: {pos_chars}")


"""
In order to easily compute the actual index of 'X' or 'AX', these utility
functions were written
"""
INDEX_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
INDEX_BASE = len(INDEX_CHARS)


def excel_column_index(index_chars: str) -> int:
    index = -1
    for i, char in enumerate(index_chars.upper()[::-1]):
        # going from right to left, the multiplicator is:
        # 26^0 = 1
        # 26^1 = 26
        index += (1 + INDEX_CHARS.index(char)) * INDEX_BASE**i

    return index


def names_to_indices(names, series):
    """translate names to indices"""
    if isinstance(names, str):
        indices = series.index(names)
    elif isinstance(names, list) and isinstance(names[0], str):
        # translate each row name to index
        indices = [series.index(astr) for astr in names]
    else:
        return names
    return indices


def abs(value):
    if value < 0:
        return value * -1

    else:
        return value
