"""
    pyexcel.internal.attributes
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Book and sheet attributes

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel.constants as constants
from pyexcel_io.constants import DB_DJANGO, DB_SQL


NO_DOT_NOTATION = (DB_DJANGO, DB_SQL)

ATTRIBUTE_REGISTRY = {
    constants.SHEET: {
        constants.READ_ACTION: set(),
        constants.WRITE_ACTION: set(),
        constants.RW_ACTION: set()
    },
    constants.BOOK: {
        constants.READ_ACTION: set(),
        constants.WRITE_ACTION: set(),
        constants.RW_ACTION: set()
    }
}


def register_an_attribute(target, action, attr):
    """Register a file type as an attribute"""
    if attr in ATTRIBUTE_REGISTRY[target][constants.RW_ACTION]:
        # No registration required
        return
    ATTRIBUTE_REGISTRY[target][action].add(attr)
    intersection = (attr in ATTRIBUTE_REGISTRY[target][constants.READ_ACTION]
                    and
                    attr in ATTRIBUTE_REGISTRY[target][constants.WRITE_ACTION])
    if intersection:
        ATTRIBUTE_REGISTRY[target][constants.RW_ACTION].add(attr)
        ATTRIBUTE_REGISTRY[target][constants.READ_ACTION].remove(attr)
        ATTRIBUTE_REGISTRY[target][constants.WRITE_ACTION].remove(attr)


def get_book_rw_attributes():
    """return read and write attributes for a book"""
    return ATTRIBUTE_REGISTRY[constants.BOOK][constants.RW_ACTION]


def get_book_w_attributes():
    """return write attributes for a book"""
    return ATTRIBUTE_REGISTRY[constants.BOOK][constants.WRITE_ACTION]


def get_book_r_attributes():
    """return read attributes for a book"""
    return ATTRIBUTE_REGISTRY[constants.BOOK][constants.READ_ACTION]


def get_sheet_rw_attributes():
    """return read and write attributes for a sheet"""
    return ATTRIBUTE_REGISTRY[constants.SHEET][constants.RW_ACTION]


def get_sheet_w_attributes():
    """return write attributes for a sheet"""
    return ATTRIBUTE_REGISTRY[constants.SHEET][constants.WRITE_ACTION]


def get_sheet_r_attributes():
    """return read attributes for a sheet"""
    return ATTRIBUTE_REGISTRY[constants.SHEET][constants.READ_ACTION]
