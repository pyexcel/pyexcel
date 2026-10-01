from copy import deepcopy

import pytest
import pyexcel as p

from .nose_tools import eq_


@pytest.mark.parametrize("left_is_book", [False, True])
@pytest.mark.parametrize("right_is_book", [False, True])
@pytest.mark.parametrize("inplace", [False, True])
@pytest.mark.parametrize(
    "array, kwargs, expected",
    [
        (
            [["Amount", "Tax"], [100, 10], [200, 20]],
            {"name_columns_by_row": 0},
            [["Amount", "Tax"], [100, 10], [200, 20]],
        ),
        (
            [[100, 10], [200, 20]],
            {"colnames": ["Amount", "Tax"]},
            [["Amount", "Tax"], [100, 10], [200, 20]],
        ),
        (
            [["one", 100, 10], ["two", 200, 20]],
            {"name_rows_by_column": 0},
            [["one", 100, 10], ["two", 200, 20]],
        ),
        (
            [["", "Amount", "Tax"], ["one", 100, 10], ["two", 200, 20]],
            {"name_columns_by_row": 0, "name_rows_by_column": 0},
            [["", "Amount", "Tax"], ["one", 100, 10], ["two", 200, 20]],
        ),
        (
            [["Amount", "Tax"]],
            {"name_columns_by_row": 0},
            [["Amount", "Tax"]],
        ),
        ([[100, 10]], {}, [[100, 10]]),
        ([], {}, []),
    ],
    ids=[
        "extracted-columns",
        "explicit-columns",
        "rows",
        "both-axes",
        "header-only",
        "plain",
        "empty",
    ],
)
def test_adding_sheets_preserves_exported_labels(
    array, kwargs, expected, left_is_book, right_is_book, inplace
):
    first = p.Sheet(deepcopy(array), "first", **deepcopy(kwargs))
    second = p.Sheet(deepcopy(array), "second", **deepcopy(kwargs))
    eq_(first.array, expected)
    eq_(p.Book({"first": first}).to_dict()["first"], expected)
    labels = [(list(s.colnames), list(s.rownames)) for s in (first, second)]
    left = (
        p.Book({"first": first}, filename="first") if left_is_book else first
    )
    right = (
        p.Book({"second": second}, filename="second")
        if right_is_book
        else second
    )

    if inplace:
        left += right
        combined = left
    else:
        combined = left + right

    first_name = "first_first" if left_is_book and not inplace else "first"
    second_name = (
        "second_second"
        if left_is_book and right_is_book and not inplace
        else "second"
    )
    eq_(combined.sheet_names(), [first_name, second_name])
    eq_(combined.to_dict(), {first_name: expected, second_name: expected})
    for sheet, (colnames, rownames) in zip((first, second), labels):
        eq_(sheet.array, expected)
        eq_(sheet.colnames, colnames)
        eq_(sheet.rownames, rownames)


def test_adding_filtered_labels():
    first = p.Sheet(
        [["", "Amount", "Tax"], ["one", 100, 10], ["two", 200, 20]],
        "first",
        name_columns_by_row=0,
        name_rows_by_column=0,
    )
    del first.row[1]
    del first.column[1]
    combined = first + p.Sheet([[300]], "second")
    eq_(combined["first"].array, [["", "Amount"], ["one", 100]])
    eq_(first.array, [["", "Amount"], ["one", 100]])


def test_adding_labelled_sheets_copies_cells_and_headers():
    first = p.Sheet([["Amount"], [100]], "first", name_columns_by_row=0)
    second = p.Sheet([["Amount"], [200]], "second", name_columns_by_row=0)
    combined = first + second
    combined["first"][0, 0] = "Edited header"
    combined["first"][1, 0] = 999
    eq_(first.array, [["Amount"], [100]])
    first.colnames[0] = "Changed source"
    first[0, 0] = 111
    eq_(combined["first"].array, [["Edited header"], [999]])
    eq_(second.array, [["Amount"], [200]])


def test_adding_labelled_sheets_with_duplicate_names():
    first = p.Sheet([["Amount"], [100]], "same", name_columns_by_row=0)
    second = p.Sheet([["Amount"], [200]], "same", name_columns_by_row=0)
    combined = first + second
    names = combined.sheet_names()
    eq_(names[0], "same")
    assert names[1].startswith("same_")
    eq_(combined[names[0]].array, [["Amount"], [100]])
    eq_(combined[names[1]].array, [["Amount"], [200]])


def test_combined_labels_round_trip_to_xlsx():
    first = p.Sheet(
        [["", "Amount", "Tax"], ["one", 100, 10]],
        "first",
        name_columns_by_row=0,
        name_rows_by_column=0,
    )
    second = p.Sheet([["Amount"], [200]], "second", name_columns_by_row=0)
    third = p.Sheet([["Amount"], [300]], "third", name_columns_by_row=0)
    combined = first + second + third
    stream = combined.save_to_memory("xlsx")
    restored = p.get_book(file_type="xlsx", file_content=stream.getvalue())
    eq_(restored.sheet_names(), ["first", "second", "third"])
    eq_(
        restored.to_dict(),
        {
            "first": [["", "Amount", "Tax"], ["one", 100, 10]],
            "second": [["Amount"], [200]],
            "third": [["Amount"], [300]],
        },
    )


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
