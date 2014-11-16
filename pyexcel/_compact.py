"""
    pyexcel._compact
    ~~~~~~~~~~~~~~~~~~~

    Compatibles

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import sys
import six


if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

if six.PY2:
    from StringIO import StringIO
else:
    from io import StringIO


def is_array_type(an_array, atype):
    tmp = [i for i in an_array if not isinstance(i, atype)]
    return len(tmp) == 0


def is_string(atype):
    """find out if a type is str or not"""
    if atype == str:
            return True
    elif six.PY2:
        if atype == unicode:
            return True
    return False
