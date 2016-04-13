from pyexcel.sources.file import SheetSource
from pyexcel.sheets import SheetStream
from pyexcel_io.manager import RWManager
from textwrap import dedent


def test_save_to():
    file_type = 'csv'
    io = RWManager.get_io(file_type)
    g = (i for i in [[1,2],[3,4]])
    ss = SheetSource((file_type, io), lineterminator='\n')
    sheet_stream = SheetStream("test", g)
    sheet_stream.save_to(ss)
    content = io.getvalue()
    expected = dedent("""\
    1,2
    3,4
    """)
    assert content == expected