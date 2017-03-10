from textwrap import dedent
import pyexcel_io.manager as manager
from pyexcel.internal.generators import SheetStream
from pyexcel.sources.file_source_output import WriteSheetToMemory


def test_save_to():
    file_type = 'csv'
    io = manager.get_io(file_type)
    g = (i for i in [[1, 2], [3, 4]])
    ss = WriteSheetToMemory(file_type=file_type, file_stream=io,
                            lineterminator='\n')
    sheet_stream = SheetStream("test", g)
    ss.write_data(sheet_stream)
    content = io.getvalue()
    expected = dedent("""\
    1,2
    3,4
    """)
    assert content == expected
