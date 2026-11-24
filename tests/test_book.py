import pyexcel as p

from .nose_tools import eq_


def test_a_dictionary_of_sheet():
    test_data = [["a", "b"]]

    book_dict = {"test": p.Sheet(test_data)}

    book = p.Book(book_dict)
    eq_(book.test.array, test_data)


def test_book_len():
    test_data = [["a", "b"]]

    book_dict = {"test": p.Sheet(test_data)}

    book = p.Book(book_dict)
    eq_(len(book.test.array), 1)


def test_sheet_ordering():
    test_data = [["a", "b"]]

    book_dict = {"first": test_data, "middle": test_data, "last": test_data}

    book = p.Book(book_dict)
    eq_(book.sheet_names(), ["first", "middle", "last"])


def test_add_named_sheets_preserves_headers():
    left = p.Sheet([["fruit", "count"], ["pear", 2]], name="left")
    left.name_columns_by_row(0)
    right = p.Sheet([["east", 3], ["west", 4]], name="right")
    right.name_rows_by_column(0)
    expected = {"left": left.to_array(), "right": right.to_array()}

    assert (left + right).to_dict() == expected
    left += right
    assert left.to_dict() == expected
