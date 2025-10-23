"""
pyexcel._compact
~~~~~~~~~~~~~~~~~~~

Compatibles

:copyright: (c) 2014-2025 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details
"""

# flake8: noqa
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=ungrouped-imports
import sys
import warnings
from io import BytesIO, StringIO
from urllib import request
from pathlib import Path
from textwrap import dedent
from itertools import zip_longest
from collections import OrderedDict

PY3_AND_ABOVE = sys.version_info[0] >= 3

Iterator = object
irange = range
czip = zip


def is_tuple_consists_of_strings(an_array):
    """check if all member were string type"""
    return isinstance(an_array, tuple) and is_array_type(an_array, str)


def is_array_type(an_array, atype):
    """check if all members are of the same type"""
    tmp = [i for i in an_array if not isinstance(i, atype)]
    return len(tmp) == 0


def is_string(atype):
    """find out if a type is str or not"""
    return atype == str


def deprecated(func, message="Deprecated!"):
    """Print deprecated message"""

    def inner(*arg, **keywords):
        """Print deperecated message"""
        warnings.warn(message, DeprecationWarning)
        return func(*arg, **keywords)

    return inner


def append_doc(value):
    def _doc(func):
        if func.__doc__:
            func.__doc__ = dedent(func.__doc__) + "\n" + value
        else:
            func.__doc__ = value
        return func

    return _doc


def get_string_file_name(file_name):
    if isinstance(file_name, Path):
        file_name = str(file_name.resolve())
    return file_name
