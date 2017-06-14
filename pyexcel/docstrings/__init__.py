"""
    pyexcel.docstrings
    ~~~~~~~~~~~~~~~~~~~

    Reusible docstrings

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from .core import (
    GET_SHEET,
    GET_BOOK,
    SAVE_AS,
    ISAVE_AS,
    SAVE_BOOK_AS,
    ISAVE_BOOK_AS,
    GET_ARRAY,
    IGET_ARRAY,
    GET_DICT,
    GET_RECORDS,
    IGET_RECORDS,
    GET_BOOK_DICT
)  # flake8: noqa

from .meta import SAVE_AS_OPTIONS

from .garbagecollector import FREE_RESOURCES
