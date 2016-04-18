from nose.tools import raises

from pyexcel.sources.base import Source
from pyexcel.sources.base import ReadOnlySource
from pyexcel.sources.base import WriteOnlySource
from pyexcel.sources.base import FileSource

from pyexcel.sources.memory import WriteOnlySheetSource
from pyexcel.sources.memory import ReadOnlySheetSource

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
def test_read_only_sheet_source():
    source = ReadOnlySheetSource()
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