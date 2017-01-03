"""
    pyexcel._compact
    ~~~~~~~~~~~~~~~~~~~

    Compatibles

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
import sys
import types
import logging

PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7

if PY26:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

if PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
    text_type = unicode
    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')
    class Iterator(object):
        def next(self):
            return type(self).__next__(self)
    import urllib2 as request
    irange = xrange
    from itertools import izip_longest as zip_longest
    from itertools import izip as czip
else:
    from io import StringIO, BytesIO
    text_type = str
    Iterator = object
    import urllib.request as request
    irange = range
    from itertools import zip_longest
    czip = zip
def is_tuple_consists_of_strings(an_array):
    return isinstance(an_array, tuple) and is_array_type(an_array, str)


def is_array_type(an_array, atype):
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


def is_generator(struct):
    return isinstance(struct, types.GeneratorType)


def deprecated(func, message="Deprecated!"):
    def inner(*arg, **keywords):
        print(message)
        return func(*arg, **keywords)
    return inner


class SheetIterator:
    """
    Sheet Iterator
    """
    def __init__(self, bookreader):
        self.book_reader_ref = bookreader
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.current < self.book_reader_ref.number_of_sheets():
            self.current += 1
            return self.book_reader_ref[self.current-1]
        else:
            raise StopIteration


def with_metaclass(meta, *bases):
    # This requires a bit of explanation: the basic idea is to make a
    # dummy metaclass for one level of class instantiation that replaces
    # itself with the actual metaclass.  Because of internal type checks
    # we also need to make sure that we downgrade the custom metaclass
    # for one level to something closer to type (that's why __call__ and
    # __init__ comes back from type etc.).
    #
    # This has the advantage over six.with_metaclass in that it does not
    # introduce dummy classes into the final MRO.
    # :copyright: (c) 2014 by Armin Ronacher.
    # :license: BSD, see LICENSE for more details.
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
