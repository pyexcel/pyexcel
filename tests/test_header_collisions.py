import pytest
from pyexcel import Sheet
from pyexcel.sheet import make_names_unique


@pytest.mark.parametrize(
    "names, expected",
    [
        (["a", "a", "a-1"], ["a", "a-2", "a-1"]),
        (["a", "a-1", "a"], ["a", "a-1", "a-2"]),
        (
            ["x", "x", "x-1", "x-2", "x"],
            ["x", "x-3", "x-1", "x-2", "x-4"],
        ),
        ([" a ", "a", "a-1 "], ["a", "a-2", "a-1"]),
        ([1, "1", "1-1"], ["1", "1-2", "1-1"]),
        (["", "", "-1"], ["", "-2", "-1"]),
    ],
)
def test_duplicate_names_do_not_replace_existing_names(names, expected):
    original = names[:]
    assert make_names_unique(names) == expected
    assert names == original


def test_unique_column_names_keep_all_record_values():
    sheet = Sheet([["a", "a", "a-1"], [1, 2, 3]], name_columns_by_row=0)
    record = next(sheet.to_records())
    assert list(record.items()) == [("a", 1), ("a-2", 2), ("a-1", 3)]


def test_unique_row_names_keep_all_record_values():
    sheet = Sheet([["a", 1], ["a", 2], ["a-1", 3]], name_rows_by_column=0)
    record = next(sheet.to_records())
    assert list(record.items()) == [("a", 1), ("a-2", 2), ("a-1", 3)]
