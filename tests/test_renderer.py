from _compact import BytesIO

from nose.tools import raises
from pyexcel.renderer import (
    Renderer,
    DbRenderer,
    BinaryRenderer,
    AbstractRenderer,
)


@raises(NotImplementedError)
def test_render_sheet():
    r = Renderer("xls")
    r.render_sheet("something")


@raises(NotImplementedError)
def test_abstract_renderer_1():
    r = AbstractRenderer("xls")
    r.render_sheet_to_file("file_name", "a sheet instance")


@raises(NotImplementedError)
def test_abstract_renderer_2():
    r = AbstractRenderer("xls")
    r.render_sheet_to_stream("file_stream", "a sheet instance")


@raises(NotImplementedError)
def test_abstract_renderer_3():
    r = AbstractRenderer("xls")
    r.render_book_to_file("file_name", "a book instance")


@raises(NotImplementedError)
def test_abstract_renderer_4():
    r = AbstractRenderer("xls")
    r.render_book_to_stream("file_stream", "a book instance")


@raises(NotImplementedError)
def test_abstract_renderer_5():
    r = AbstractRenderer("xls")
    r.get_io()


@raises(Exception)
def test_db_renderer_1():
    r = DbRenderer("xls")
    r.render_sheet_to_file("file_name", "a sheet")


@raises(Exception)
def test_db_renderer_2():
    r = DbRenderer("xls")
    r.render_book_to_file("file_name", "a book")


def test_binary_renderer():
    r = BinaryRenderer("abc")
    io = r.get_io()
    assert isinstance(io, BytesIO)
