import pyexcel.sources as factory
from pyexcel.internal.generators import BookStream, SheetStream
from pyexcel._compact import PY2


def get_sheet_stream(**keywords):
    """
    Get an instance of SheetStream from an excel source
    """
    source = factory.get_source(**keywords)
    sheets = source.get_data()
    sheet_name, data = one_sheet_tuple(sheets.items())
    return SheetStream(sheet_name, data)


def get_book_stream(**keywords):
    """
    Get an instance of BookStream from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    source = factory.get_book_source(**keywords)
    sheets = source.get_data()
    filename, path = source.get_source_info()
    return BookStream(sheets, filename=filename, path=path)


def save_sheet(sheet, **keywords):
    """
    Save a sheet instance to any source
    """
    source = factory.get_writable_source(**keywords)
    return _save_any(source, sheet)


def save_book(book, **keywords):
    """
    Save a book instance to any source
    """
    source = factory.get_writable_book_source(**keywords)
    return _save_any(source, book)


def _save_any(source, instance):
    source.write_data(instance)
    try:
        content_stream = source.get_internal_stream()
        _try_put_file_read_pointer_to_its_begining(content_stream)
        return content_stream
    except NotImplementedError:
        return None


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
