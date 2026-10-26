import pytest
from pyexcel import Sheet


@pytest.mark.parametrize("index", [0, 1, 3, -1])
def test_delete_named_column_by_index_preserves_row_names(index):
    data = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    sheet = Sheet(
        data, colnames=["a", "b", "c", "d"], rownames=["x", "y", "z"]
    )
    expected_data = [row[:] for row in data]
    expected_columns = sheet.colnames[:]
    for row in expected_data:
        del row[index]
    del expected_columns[index]

    sheet.delete_named_column_at(index)

    assert sheet.get_internal_array() == expected_data
    assert sheet.colnames == expected_columns
    assert sheet.rownames == ["x", "y", "z"]
    assert sheet.row["y"] == expected_data[1]


@pytest.mark.parametrize("index", [0, 1, 2, -1])
def test_delete_named_row_by_index_removes_one_label(index):
    data = [[1, 2], [3, 4], [5, 6]]
    sheet = Sheet(data, colnames=["a", "b"], rownames=["x", "y", "z"])
    expected_data = [row[:] for row in data]
    expected_rows = sheet.rownames[:]
    del expected_data[index]
    del expected_rows[index]

    sheet.delete_named_row_at(index)

    assert sheet.get_internal_array() == expected_data
    assert sheet.rownames == expected_rows
    assert sheet.colnames == ["a", "b"]
    for name, row in zip(expected_rows, expected_data):
        assert sheet.row[name] == row


@pytest.mark.parametrize(
    "method", ["delete_named_column_at", "delete_named_row_at"]
)
def test_delete_only_named_axis_item(method):
    sheet = Sheet([[1]], colnames=["a"], rownames=["x"])

    getattr(sheet, method)(0)

    if method == "delete_named_column_at":
        assert sheet.colnames == []
        assert sheet.rownames == ["x"]
    else:
        assert sheet.rownames == []
        assert sheet.colnames == ["a"]
