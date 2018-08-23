from nose.tools import raises

from pyexcel.source import AbstractSource
from pyexcel.plugins.sources.output_to_memory import WriteSheetToMemory
from pyexcel.plugins import FileSourceInfo


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


def test_file_source_info_with_file_type():
    class CustomInfo(FileSourceInfo):
        fields = ['test']

        def can_i_handle(self, action, file_type):
            return file_type == 'csv'

    info = CustomInfo('apth')
    expected = info.is_my_business('READ',
                                   test='unit',
                                   file_name="unknow.file",
                                   file_type="csv")
    assert expected
