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

attribute_registry = {
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
    if attr in attribute_registry[target][constants.RW_ACTION]:
        # No registration required
        return
    attribute_registry[target][action].add(attr)
    intersection = (attr in attribute_registry[target][constants.READ_ACTION]
                    and
                    attr in attribute_registry[target][constants.WRITE_ACTION])
    if intersection:
        attribute_registry[target][constants.RW_ACTION].add(attr)
        attribute_registry[target][constants.READ_ACTION].remove(attr)
        attribute_registry[target][constants.WRITE_ACTION].remove(attr)


def get_book_rw_attributes():
    """return read and write attributes for a book"""
    return attribute_registry[constants.BOOK][constants.RW_ACTION]


def get_book_w_attributes():
    """return write attributes for a book"""
    return attribute_registry[constants.BOOK][constants.WRITE_ACTION]


def get_book_r_attributes():
    """return read attributes for a book"""
    return attribute_registry[constants.BOOK][constants.READ_ACTION]


def get_sheet_rw_attributes():
    """return read and write attributes for a sheet"""
    return attribute_registry[constants.SHEET][constants.RW_ACTION]


def get_sheet_w_attributes():
    """return write attributes for a sheet"""
    return attribute_registry[constants.SHEET][constants.WRITE_ACTION]


def get_sheet_r_attributes():
    """return read attributes for a sheet"""
    return attribute_registry[constants.SHEET][constants.READ_ACTION]
