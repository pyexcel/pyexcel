from textwrap import dedent

from pyexcel.internal.common import get_sheet_headers
from pyexcel.internal.generators import SheetStream
from pyexcel.plugins.sources.output_to_memory import WriteSheetToMemory

import pyexcel_io.manager as manager
from nose.tools import eq_


def test_save_to():
    file_type = "csv"
    io = manager.get_io(file_type)
    g = (i for i in [[1, 2], [3, 4]])
    ss = WriteSheetToMemory(
        file_type=file_type, file_stream=io, lineterminator="\n"
    )
    sheet_stream = SheetStream("test", g)
    ss.write_data(sheet_stream)
    content = io.getvalue()
    expected = dedent(
        """\
    1,2
    3,4
    """
    )
    assert content == expected


def test_get_sheet_headers():
    data = iter([["a", "b", "c"], [1, 2, 3]])
    sheet_stream = SheetStream("test", data)
    colnames_array = get_sheet_headers(sheet_stream)
    eq_(colnames_array, ["a", "b", "c"])
