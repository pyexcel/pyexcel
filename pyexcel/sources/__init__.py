# flake8: noqa
from . import file_source_output, database
from . import file_source_input, http, pydata
from . import factory
from pyexcel._compact import PY2
from pyexcel.generators import BookStream, SheetStream
import pyexcel.constants as constants


def get_sheet_stream(**keywords):
    source = factory.get_source(**keywords)
    sheets = source.get_data()
    sheet_name, data = one_sheet_tuple(sheets.items())
    return SheetStream(sheet_name, data)


def get_book_stream(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    source = factory.get_book_source(**keywords)
    sheets = source.get_data()
    filename, path = source.get_source_info()
    book = BookStream(sheets, filename=filename, path=path)
    return book


def save_sheet(sheet, **keywords):
    source = factory.get_writable_source(**keywords)
    source.write_data(sheet)
    if hasattr(source, 'content'):
        _try_put_file_read_pointer_to_its_begining(source.content)
        return source.content


def save_book(book, **keywords):
    source = factory.get_writable_book_source(**keywords)
    source.write_data(book)
    if hasattr(source, 'content'):
        _try_put_file_read_pointer_to_its_begining(source.content)
        return source.content


def register_presentation(cls, file_type):
    getter = presenter(file_type)
    file_type_property = property(
        getter,
        doc=constants._OUT_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
    setattr(cls, file_type, file_type_property)
    setattr(cls, 'get_%s' % file_type, getter)


def register_io(cls, file_type):
    getter = presenter(file_type)
    setter = importer(file_type)
    file_type_property = property(
        getter, setter,
        doc=constants._IO_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
    setattr(cls, file_type, file_type_property)
    setattr(cls, 'get_%s' % file_type, getter)
    setattr(cls, 'set_%s' % file_type, setter)


class SheetMeta(type):
    def __init__(cls, name, bases, nmspc):
        super(SheetMeta, cls).__init__(name, bases, nmspc)
        for attribute in factory.get_sheet_rw_attributes():
            register_io(cls, attribute)
        for attribute in factory.get_sheet_w_attributes():
            register_presentation(cls, attribute)
        setattr(cls, "register_io", classmethod(register_io))
        setattr(cls, "register_presentation", classmethod(register_presentation))


def register_book_presentation(cls, file_type):
    getter = book_presenter(file_type)
    file_type_property = property(
        getter,
        doc=constants._OUT_FILE_TYPE_DOC_STRING.format(file_type, "Book"))
    setattr(cls, file_type, file_type_property)
    setattr(cls, 'get_%s' % file_type, getter)


def register_book_io(cls, file_type):
    getter = book_presenter(file_type)
    setter = book_importer(file_type)
    file_type_property = property(
        getter, setter,
        doc=constants._IO_FILE_TYPE_DOC_STRING.format(file_type, "Book"))
    setattr(cls, file_type, file_type_property)
    setattr(cls, 'get_%s' % file_type, getter)
    setattr(cls, 'set_%s' % file_type, setter)


class BookMeta(type):
    def __init__(cls, name, bases, nmspc):
        super(BookMeta, cls).__init__(name, bases, nmspc)
        for attribute in factory.get_book_rw_attributes():
            register_book_io(cls, attribute)
        for attribute in factory.get_book_w_attributes():
            register_book_presentation(cls, attribute)
        setattr(cls, "register_io", classmethod(register_book_io))
        setattr(cls, "register_presentation", classmethod(register_book_presentation))


def presenter(attribute=None):
    def custom_presenter(self, **keywords):
        keyword = _get_keyword_for_parameter(attribute)
        keywords[keyword] = attribute
        memory_source = factory.get_writable_source(**keywords)
        memory_source.write_data(self)
        return memory_source.content.getvalue()
    return custom_presenter


def importer(attribute=None):
    def custom_presenter1(self, content, **keywords):
        sheet_params = {}
        for field in constants.VALID_SHEET_PARAMETERS:
            if field in keywords:
                sheet_params[field] = keywords.pop(field)
        keyword = _get_keyword_for_parameter(attribute)
        if keyword == "file_type":
            keywords[keyword] = attribute
            keywords["file_content"] = content
        else:
            keywords[keyword] = content
        named_content = get_sheet_stream(**keywords)
        self.init(named_content.payload,
                  named_content.name, **sheet_params)

    return custom_presenter1


def book_presenter(attribute=None):
    def custom_presenter(self, **keywords):
        keyword = _get_keyword_for_parameter(attribute)
        keywords[keyword] = attribute
        memory_source = factory.get_writable_book_source(**keywords)
        memory_source.write_data(self)
        return memory_source.content.getvalue()
    return custom_presenter


def book_importer(attribute=None):
    def custom_book_importer(self, content, **keywords):
        keyword = _get_keyword_for_parameter(attribute)
        if keyword == "file_type":
            keywords[keyword] = attribute
            keywords["file_content"] = content
        else:
            keywords[keyword] = content
        sheets, filename, path = _get_book(**keywords)
        self.init(sheets=sheets, filename=filename, path=path)

    return custom_book_importer


def _get_book(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    source = factory.get_book_source(**keywords)
    sheets = source.get_data()
    filename, path = source.get_source_info()
    return sheets, filename, path


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


def _get_keyword_for_parameter(key):
    return factory.keywords.get(key, None)
