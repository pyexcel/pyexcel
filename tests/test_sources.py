from nose.tools import raises, eq_

from pyexcel.source import AbstractSource
from pyexcel.plugins.sources.file_sources import (
    FileSource,
    InputSource,
    OutputSource)

from pyexcel.plugins.sources.output_to_memory import WriteSheetToMemory


def test_io_source():
    status = OutputSource.can_i_handle("read", "xls")
    eq_(status, False)


def test_input_source():
    status = InputSource.can_i_handle("write", "xls")
    eq_(status, False)


def test_source():
    source = AbstractSource(source="asource", params="params")
    info = source.get_source_info()
    assert info, (None, None)


def test_source_class_method():
    assert AbstractSource.is_my_business('read', source="asource") is True
    assert AbstractSource.is_my_business('read', file_name="asource") is False


@raises(Exception)
def test_read_only_source():
    source = AbstractSource()
    source.write_data("something")


@raises(Exception)
def test_write_only_source():
    source = AbstractSource()
    source.get_data()


@raises(Exception)
def test_write_only_sheet_source():
    source = WriteSheetToMemory()
    source.get_data()


def test_file_source_class_method():
    assert FileSource.can_i_handle('read', "csv") is False
    assert FileSource.can_i_handle('write', "csv") is False
    assert FileSource.can_i_handle('wrong action', "csv") is False
