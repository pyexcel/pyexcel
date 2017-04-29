"""
    pyexcel.internal.meta
    ~~~~~~~~~~~~~~~~~~~~~~

    Annotate sheet and book class' attributes

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from functools import partial

from pyexcel.internal import SOURCE
import pyexcel.constants as constants
from pyexcel.internal.core import get_sheet_stream
from pyexcel.internal.common import PyexcelObject


def make_presenter(source_getter, attribute=None):
    """make a custom presentation method for each file types
    """
    def custom_presenter(self, **keywords):
        """docstring is assigned a few lines down the line"""
        keyword = SOURCE.get_keyword_for_parameter(attribute)
        keywords[keyword] = attribute
        memory_source = source_getter(**keywords)
        memory_source.write_data(self)
        try:
            content_stream = memory_source.get_content()
            content = content_stream.getvalue()
        except AttributeError:
            # python 3 _io.TextWrapper
            content = None

        return content
    custom_presenter.__doc__ = "Get data in %s format" % attribute
    return custom_presenter


def sheet_presenter(attribute=None):
    """make a custom presentation method for sheet
    """
    source_getter = SOURCE.get_writable_source
    return make_presenter(source_getter, attribute)


def book_presenter(attribute=None):
    """make a custom presentation method for book
    """
    source_getter = SOURCE.get_writable_book_source
    return make_presenter(source_getter, attribute)


def importer(attribute=None):
    """make a custom input method for sheet
    """
    def custom_importer1(self, content, **keywords):
        """docstring is assigned a few lines down the line"""
        sheet_params = {}
        for field in constants.VALID_SHEET_PARAMETERS:
            if field in keywords:
                sheet_params[field] = keywords.pop(field)
        keyword = SOURCE.get_keyword_for_parameter(attribute)
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
    """make a custom input method for book
    """
    def custom_book_importer(self, content, **keywords):
        """docstring is assigned a few lines down the line"""
        keyword = SOURCE.get_keyword_for_parameter(attribute)
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
    """a default method for missing renderer method

    for example, the support to write data in a specific file type
    is missing but the support to read data exists
    """
    def none_presenter(_, **__):
        """docstring is assigned a few lines down the line"""
        raise NotImplementedError("%s getter is not defined." % attribute)
    none_presenter.__doc__ = "%s getter is not defined." % attribute
    return none_presenter


def default_importer(attribute=None):
    """a default method for missing parser method

    for example, the support to read data in a specific file type
    is missing but the support to write data exists
    """
    def none_importer(_, __, **___):
        """docstring is assigned a few lines down the line"""
        raise NotImplementedError("%s setter is not defined." % attribute)
    none_importer.__doc__ = "%s setter is not defined." % attribute
    return none_importer


class StreamAttribute(object):
    """Provide access to get_*_stream methods"""
    def __init__(self, cls):
        self.cls = cls

    def __getattr__(self, name):
        getter = getattr(self.cls, 'save_to_memory')
        return getter(file_type=name)


def _annotate_pyexcel_object_attribute(
        cls, file_type, presenter_func=sheet_presenter,
        input_func=default_importer,
        instance_name="Sheet",
        description=constants.OUT_FILE_TYPE_DOC_STRING):
    getter = presenter_func(file_type)
    setter = input_func(file_type)
    file_type_property = property(
        # note:
        # without fget, fset, pypy 5.4.0 crashes randomly.
        fget=getter, fset=setter,
        doc=description.format(file_type,
                               instance_name))
    if '.' in file_type:
        attribute = file_type.replace('.', '_')
    else:
        attribute = file_type
    setattr(cls, attribute, file_type_property)
    setattr(cls, 'get_%s' % attribute, getter)
    setattr(cls, 'set_%s' % attribute, setter)
    if file_type == 'html' and instance_name == "Sheet":
        def repr_html(self):
            """jupyter note book html representation"""
            html = getter(self)
            return html
        setattr(cls, '_repr_html_', repr_html)
    if file_type == 'svg':
        def plot_svg(self, **keywords):
            """jupyter note book svg representation"""
            return self.save_to_memory('svg', **keywords)

        setattr(cls, 'plot', plot_svg)


REGISTER_PRESENTATION = _annotate_pyexcel_object_attribute
REGISTER_BOOK_PRESENTATION = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=book_presenter,
    instance_name="Book")
REGISTER_INPUT = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=default_presenter,
    input_func=importer,
    description=constants.IN_FILE_TYPE_DOC_STRING)
REGISTER_BOOK_INPUT = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=default_presenter,
    input_func=book_importer,
    instance_name="Book",
    description=constants.IN_FILE_TYPE_DOC_STRING)
REGISTER_IO = partial(
    _annotate_pyexcel_object_attribute,
    input_func=importer,
    description=constants.IO_FILE_TYPE_DOC_STRING)
REGISTER_BOOK_IO = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=book_presenter,
    input_func=book_importer,
    instance_name="Book",
    description=constants.IO_FILE_TYPE_DOC_STRING)


class SheetMeta(PyexcelObject):
    """Annotate sheet attributes"""
    pass


setattr(SheetMeta, "register_io", classmethod(REGISTER_IO))
setattr(SheetMeta, "register_presentation", classmethod(REGISTER_PRESENTATION))
setattr(SheetMeta, "register_input", classmethod(REGISTER_INPUT))


class BookMeta(PyexcelObject):
    """Annotate book attributes"""
    pass


setattr(BookMeta, "register_io", classmethod(REGISTER_BOOK_IO))
setattr(BookMeta, "register_presentation",
        classmethod(REGISTER_BOOK_PRESENTATION))
setattr(BookMeta, "register_input",
        classmethod(REGISTER_BOOK_INPUT))


def _get_book(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    a_source = SOURCE.get_book_source(**keywords)
    sheets = a_source.get_data()
    filename, path = a_source.get_source_info()
    return sheets, filename, path
