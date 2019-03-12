from pyexcel._compact import PY2
from pyexcel.internal.core import _seek_at_zero

from mock import MagicMock


def test_seek_at_zero():
    stream = MagicMock()
    if PY2:
        stream.seek.side_effect = IOError()
    else:
        import io

        stream.seek.side_effect = io.UnsupportedOperation()
    _seek_at_zero(stream)
