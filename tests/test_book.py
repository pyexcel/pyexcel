import pyexcel as p
from nose.tools import eq_


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
