from pyexcel.internal.generators import BookStream


def test_book_stream():
    bs = BookStream()
    assert bs.number_of_sheets() == 0


def test_load_from_empty_sheets():
    bs = BookStream()
    bs.load_from_sheets(None)
    assert bs.number_of_sheets() == 0


def test_key_sorting():
    adict = {
        "cd": [[1, 3]],
        "ab": [[2, 3]]
    }
    bs = BookStream(adict)
    # bs[0] should be 'ab' : SheetStream([[2,3]])
    assert bs[0].payload == [[2, 3]]
