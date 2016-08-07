# flake8: noqa
from . import file_source_output, database
from . import file_source_input, http, pydata
from .factory import Source


def get_book_rw_attributes():
    return set(Source.attribute_registry["book-read"]).intersection(
        set(Source.attribute_registry["book-write"]))


def get_book_w_attributes():
    return set(Source.attribute_registry["book-write"]).difference(
        set(Source.attribute_registry["book-read"]))


def get_sheet_rw_attributes():
    return set(Source.attribute_registry["sheet-read"]).intersection(
        set(Source.attribute_registry["sheet-write"]))


def get_sheet_w_attributes():
    return set(Source.attribute_registry["sheet-write"]).difference(
        set(Source.attribute_registry["sheet-read"]))


def _get_generic_source(target, action, **keywords):
    key = "%s-%s" % (target, action)
    for source in Source.registry[key]:
        if source.is_my_business(action, **keywords):
            s = source(**keywords)
            return s
    return None


def get_source(**keywords):
    source = _get_generic_source(
        'input',
        'read',
        **keywords)
    if source is None:
        source = _get_generic_source(
            'sheet',
            'read',
            **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_book_source(**keywords):
    source = _get_generic_source(
        'input',
        'read',
        **keywords)
    if source is None:
        source = _get_generic_source(
            'book',
            'read',
            **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_writable_source(**keywords):
    source = _get_generic_source(
        'sheet',
        'write',
        **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_writable_book_source(**keywords):
    source = _get_generic_source(
        'book',
        'write',
        **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source
