import io
from unittest.mock import MagicMock

from pyexcel.internal.core import _seek_at_zero


def test_seek_at_zero():
    stream = MagicMock()
    stream.seek.side_effect = io.UnsupportedOperation()
    _seek_at_zero(stream)
