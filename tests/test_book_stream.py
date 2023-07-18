from pyexcel.internal.common import get_book_headers_in_array
from pyexcel.internal.generators import BookStream

from nose.tools import eq_


def test_book_stream():
    bs = BookStream()
    assert bs.number_of_sheets() == 0


def test_load_from_empty_sheets():
    bs = BookStream()
    bs.load_from_sheets(None)
    assert bs.number_of_sheets() == 0


def test_key_sorting():
    adict = {"cd": [[1, 3]], "ab": [[2, 3]]}
    bs = BookStream(adict)
    # bs[0] should be 'ab' : SheetStream([[2,3]])
    assert bs[0].payload == [[2, 3]]


def test_get_book_headers_in_array():
    data = iter([["a", "b", "c"], [1, 2, 3]])
    book_stream = BookStream({"test": data})
    colnames_array = get_book_headers_in_array(book_stream)
    eq_(colnames_array, [["a", "b", "c"]])
