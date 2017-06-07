"""
    pyexcel._compact
    ~~~~~~~~~~~~~~~~~~~

    Compatibles

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=invalid-name
# pylint: disable=redefined-variable-type
# pylint: disable=too-few-public-methods
# pylint: disable=ungrouped-imports
import sys
import warnings
from textwrap import dedent

PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7
PY3_AND_ABOVE = sys.version_info[0] >= 3

if PY26:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

if PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
    from itertools import izip_longest as zip_longest
    from itertools import izip as czip
    import urllib2 as request

    class Iterator(object):
        """Python 2 iterator"""
        def next(self):
            """Iterator interface get next value"""
            return type(self).__next__(self)
    irange = xrange
else:
    from io import StringIO, BytesIO
    import urllib.request as request
    from itertools import zip_longest
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
    if atype == str:
        return True
    elif PY2:
        if atype == unicode:
            return True
    return False


def deprecated(func, message="Deprecated!"):
    """Print deprecated message"""
    def inner(*arg, **keywords):
        """Print deperecated message"""
        warnings.warn(message, DeprecationWarning)
        return func(*arg, **keywords)
    return inner


def append_doc(value):
    def _doc(func):
        func.__doc__ = dedent(func.__doc__) + '\n' + value
        return func
    return _doc
