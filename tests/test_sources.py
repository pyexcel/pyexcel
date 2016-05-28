from nose.tools import raises, eq_

from pyexcel.factory import Source, ReadOnlySource
from pyexcel.factory import FileSource, WriteOnlySource

from pyexcel.sources.file_source_output import WriteOnlySheetSource
from pyexcel.sources.file_source_output import IOSource
from pyexcel.sources.file_source_input import InputSource


def test_io_source():
    status = IOSource.can_i_handle("read", "xls")
    eq_(status, False)


def test_input_source():
    status = InputSource.can_i_handle("write", "xls")
    eq_(status, False)


def test_source():
    source = Source(source="asource", params="params")
    assert source.keywords == {"params": "params"}
    assert source.source == "asource"


def test_source_class_method():
    assert Source.is_my_business('read', source="asource") == True
    assert Source.is_my_business('read', file_name="asource") == False


@raises(Exception)
def test_read_only_source():
    source = ReadOnlySource()
    source.write_data("something")



@raises(Exception)
def test_write_only_source():
    source = WriteOnlySource()
    source.get_data()


@raises(Exception)
def test_write_only_sheet_source():
    source = WriteOnlySheetSource()
    source.get_data()


def test_file_source_class_method():
    assert FileSource.can_i_handle('read', "csv") == False
    assert FileSource.can_i_handle('write', "csv") == False
    assert FileSource.can_i_handle('wrong action', "csv") == False