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
    from .meta import SheetMeta, BookMeta

    if attr in ATTRIBUTE_REGISTRY[target][constants.RW_ACTION]:
        # No registration required
        return
    ATTRIBUTE_REGISTRY[target][action].add(attr)
    if target == 'book':
        meta_cls = BookMeta
    elif target == 'sheet':
        meta_cls = SheetMeta
    else:
        raise Exception("Known target: %s" % target)

    if action == constants.READ_ACTION:
        meta_cls.register_input(attr)
    else:
        meta_cls.register_presentation(attr)

    intersection = (attr in ATTRIBUTE_REGISTRY[target][constants.READ_ACTION]
                    and
                    attr in ATTRIBUTE_REGISTRY[target][constants.WRITE_ACTION])
    if intersection:
        ATTRIBUTE_REGISTRY[target][constants.RW_ACTION].add(attr)
        ATTRIBUTE_REGISTRY[target][constants.READ_ACTION].remove(attr)
        ATTRIBUTE_REGISTRY[target][constants.WRITE_ACTION].remove(attr)
        meta_cls.register_io(attr)
