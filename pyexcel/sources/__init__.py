from functools import partial
from . import file_source_output, database  # noqa
from . import file_source_input, http, pydata  # noqa
from . import factory
from pyexcel._compact import PY2
from pyexcel.generators import BookStream, SheetStream
import pyexcel.constants as constants


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


def make_presenter(source_getter, attribute=None):
    def custom_presenter(self, **keywords):
        keyword = _get_keyword_for_parameter(attribute)
        keywords[keyword] = attribute
        memory_source = source_getter(**keywords)
        memory_source.write_data(self)
        try:
            content_stream = memory_source.get_internal_stream()
            content = content_stream.getvalue()
        except AttributeError:
            # python 3 _io.TextWrapper
            content = None
        return content
    custom_presenter.__doc__ = "Get data in %s format" % attribute
    return custom_presenter


def sheet_presenter(attribute=None):
    source_getter = factory.get_writable_source
    return make_presenter(source_getter, attribute)


def book_presenter(attribute=None):
    source_getter = factory.get_writable_book_source
    return make_presenter(source_getter, attribute)


def importer(attribute=None):
    def custom_importer1(self, content, **keywords):
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
    custom_importer1.__doc__ = "Set data in %s format" % attribute
    return custom_importer1


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
    custom_book_importer.__doc__ = "Set data in %s format" % attribute
    return custom_book_importer


def default_presenter(attribute=None):
    def none_presenter(self, **keywords):
        raise NotImplementedError("%s getter is not defined." % attribute)
    none_presenter.__doc__ = "%s getter is not defined." % attribute
    return none_presenter


def default_importer(attribute=None):
    def none_importer(self, content, **keywords):
        raise NotImplementedError("%s setter is not defined." % attribute)
    none_importer.__doc__ = "%s setter is not defined." % attribute
    return none_importer


class StreamAttribute:
    """Provide access to get_*_stream methods"""
    def __init__(self, cls):
        self.cls = cls

    def __getattr__(self, name):
        getter = getattr(self.cls, 'save_to_memory')
        return getter(file_type=name)


def _register_instance_input_and_output(
        cls, file_type, presenter_func=sheet_presenter,
        input_func=default_importer,
        instance_name="Sheet",
        description=constants._OUT_FILE_TYPE_DOC_STRING):
    getter = presenter_func(file_type)
    setter = input_func(file_type)
    file_type_property = property(
        # note:
        # without fget, fset, pypy 5.4.0 crashes randomly.
        fget=getter, fset=setter,
        doc=description.format(file_type,
                               instance_name))
    setattr(cls, file_type, file_type_property)
    setattr(cls, 'get_%s' % file_type, getter)
    setattr(cls, 'set_%s' % file_type, setter)


register_presentation = _register_instance_input_and_output
register_book_presentation = partial(
    _register_instance_input_and_output,
    presenter_func=book_presenter,
    instance_name="Book")
register_input = partial(
    _register_instance_input_and_output,
    presenter_func=default_presenter,
    input_func=importer,
    description=constants._IN_FILE_TYPE_DOC_STRING)
register_book_input = partial(
    _register_instance_input_and_output,
    presenter_func=default_presenter,
    input_func=book_importer,
    instance_name="Book",
    description=constants._IN_FILE_TYPE_DOC_STRING)
register_io = partial(
    _register_instance_input_and_output,
    input_func=importer,
    description=constants._IO_FILE_TYPE_DOC_STRING)
register_book_io = partial(
    _register_instance_input_and_output,
    presenter_func=book_presenter,
    input_func=book_importer,
    instance_name="Book",
    description=constants._IO_FILE_TYPE_DOC_STRING)


class SheetMeta(type):
    def __init__(cls, name, bases, nmspc):
        super(SheetMeta, cls).__init__(name, bases, nmspc)
        for attribute in factory.get_sheet_rw_attributes():
            register_io(cls, attribute)
        for attribute in factory.get_sheet_w_attributes():
            register_presentation(cls, attribute)
        for attribute in factory.get_sheet_r_attributes():
            register_input(cls, attribute)
        setattr(cls, "register_io", classmethod(register_io))
        setattr(cls, "register_presentation",
                classmethod(register_presentation))
        setattr(cls, "register_input",
                classmethod(register_input))


class BookMeta(type):
    def __init__(cls, name, bases, nmspc):
        super(BookMeta, cls).__init__(name, bases, nmspc)
        for attribute in factory.get_book_rw_attributes():
            register_book_io(cls, attribute)
        for attribute in factory.get_book_w_attributes():
            register_book_presentation(cls, attribute)
        for attribute in factory.get_book_r_attributes():
            register_book_input(cls, attribute)
        setattr(cls, "register_io", classmethod(register_book_io))
        setattr(cls, "register_presentation",
                classmethod(register_book_presentation))
        setattr(cls, "register_book_input",
                classmethod(register_book_input))


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
