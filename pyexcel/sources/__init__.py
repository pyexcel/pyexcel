# flake8: noqa
from . import file_source_output, database
from . import file_source_input, http, pydata
from .factory import Source
from pyexcel._compact import PY2
from pyexcel.generators import BookStream, SheetStream


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


def get_sheet_stream(**keywords):
    source = get_source(**keywords)
    sheets = source.get_data()
    sheet_name, data = one_sheet_tuple(sheets.items())
    return SheetStream(sheet_name, data)


def get_book_stream(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    source = get_book_source(**keywords)
    sheets = source.get_data()
    filename, path = source.get_source_info()
    book = BookStream(sheets, filename=filename, path=path)
    return book


def save_sheet(sheet, **keywords):
    source = get_writable_source(**keywords)
    source.write_data(sheet)
    if hasattr(source, 'content'):
        _try_put_file_read_pointer_to_its_begining(source.content)
        return source.content

        
def save_book(book, **keywords):
    source = get_writable_book_source(**keywords)
    source.write_data(book)
    if hasattr(source, 'content'):
        _try_put_file_read_pointer_to_its_begining(source.content)
        return source.content


def _try_put_file_read_pointer_to_its_begining(a_stream):
    if PY2:
        try:
            a_stream.seek(0)
        except IOError:
            pass
    else:
        import io
        try:
            a_stream.seek(0)
        except io.UnsupportedOperation:
            pass


def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    return items[0][0], items[0][1]

