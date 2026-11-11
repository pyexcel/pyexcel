import copy

import pytest
from pyexcel import Sheet


@pytest.mark.parametrize("copy_sheet", [Sheet.clone, copy.deepcopy])
@pytest.mark.parametrize(
    "data, options",
    [
        ([], {}),
        ([["Alice", 100], ["Bob", 200]], {}),
        (
            [["account", "balance"], ["Alice", 100], ["Bob", 200]],
            {"name_columns_by_row": 0},
        ),
        ([["Alice", 100], ["Bob", 200]], {"name_rows_by_column": 0}),
        (
            [["", "balance"], ["Alice", 100], ["Bob", 200]],
            {"name_columns_by_row": 0, "name_rows_by_column": 0},
        ),
        (
            [[100], [200]],
            {"colnames": ["balance"], "rownames": ["Alice", "Bob"]},
        ),
        ([["account", "balance"]], {"name_columns_by_row": 0}),
        ([["Alice"], ["Bob"]], {"name_rows_by_column": 0}),
        (
            [["Alice", 100], ["account", "balance"], ["Bob", 200]],
            {"name_columns_by_row": 1},
        ),
        ([[100, "Alice"], [200, "Bob"]], {"name_rows_by_column": 1}),
    ],
)
def test_copy_preserves_current_sheet(data, options, copy_sheet):
    sheet = Sheet(copy.deepcopy(data), name="accounts", **options)
    array = copy.deepcopy(sheet.get_internal_array())
    colnames, rownames = sheet.colnames[:], sheet.rownames[:]

    copied = copy_sheet(sheet)

    assert copied.get_internal_array() == array
    assert copied.colnames == colnames
    assert copied.rownames == rownames
    assert copied.name == sheet.name
    assert copied.number_of_rows() == sheet.number_of_rows()
    assert copied.number_of_columns() == sheet.number_of_columns()
    assert copied.get_internal_array() is not sheet.get_internal_array()
    assert copied.colnames is not sheet.colnames
    assert copied.rownames is not sheet.rownames
    if copied.number_of_rows() and copied.number_of_columns():
        copied[0, 0] = "changed"
    copied.colnames.append("changed")
    copied.rownames.append("changed")
    assert sheet.get_internal_array() == array
    assert sheet.colnames == colnames
    assert sheet.rownames == rownames


@pytest.mark.parametrize("copy_sheet", [Sheet.clone, copy.deepcopy])
@pytest.mark.parametrize("transpose", [False, True])
def test_copy_after_filtering_and_transposing(copy_sheet, transpose):
    sheet = Sheet(
        [["", "balance", "fee"], ["Alice", 100, 5], ["Bob", 200, 6]],
        name="accounts",
        name_columns_by_row=0,
        name_rows_by_column=0,
    )
    sheet.filter(row_indices=[0], column_indices=[1])
    if transpose:
        sheet.transpose()

    copied = copy_sheet(sheet)

    assert copied.to_array() == sheet.to_array()
    assert copied.get_internal_array() == sheet.get_internal_array()
    assert copied.colnames == sheet.colnames
    assert copied.rownames == sheet.rownames
    assert copied.name == sheet.name


@pytest.mark.parametrize("copy_sheet", [Sheet.clone, copy.deepcopy])
def test_copy_nested_cell_is_independent(copy_sheet):
    sheet = Sheet([[{"values": [100]}]], colnames=["balance"])

    copied = copy_sheet(sheet)
    copied[0, 0]["values"].append(200)

    assert sheet[0, 0] == {"values": [100]}


def test_row_addition_preserves_named_sheet():
    sheet = Sheet([["balance"], [100]], name="accounts", name_columns_by_row=0)

    copied = sheet.row + [[200]]

    assert copied.get_internal_array() == [[100], [200]]
    assert copied.colnames == ["balance"]
    assert copied.name == "accounts"
    assert sheet.get_internal_array() == [[100]]


def test_column_addition_preserves_named_sheet():
    sheet = Sheet([["Alice", 100]], name="accounts", name_rows_by_column=0)

    copied = sheet.column + [[5]]

    assert copied.get_internal_array() == [[100, 5]]
    assert copied.rownames == ["Alice"]
    assert copied.name == "accounts"
    assert sheet.get_internal_array() == [[100]]
