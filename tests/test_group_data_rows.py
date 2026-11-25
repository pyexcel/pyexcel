import pytest
from pyexcel import Sheet


@pytest.mark.parametrize("column", [0, -2])
def test_grouping_by_index_matches_named_column(column):
    sheet = Sheet(
        [["kind", "value"], ["x", 1], ["y", 2], ["x", 3]],
        name_columns_by_row=0,
    )
    expected = sheet.group_rows_by_column("kind").to_dict()
    assert sheet.group_rows_by_column(column).to_dict() == expected
    assert list(expected) == ["x", "y"]
    assert expected["x"] == [["kind", "value"], ["x", 1], ["x", 3]]


def test_grouping_without_labels_preserves_data_rows():
    sheet = Sheet([["x", 1], ["y", 2], ["x", 3]])
    assert sheet.group_rows_by_column(0).to_dict() == {
        "x": [["x", 1], ["x", 3]],
        "y": [["y", 2]],
    }


def test_grouping_by_index_uses_data_columns_with_row_names():
    sheet = Sheet([["x", 1], ["x", 2]], rownames=["first", "second"])
    assert sheet.group_rows_by_column(0).to_dict() == {
        "x": [["x", 1], ["x", 2]]
    }


def test_header_only_sheet_has_no_groups():
    sheet = Sheet([["kind", "value"]], name_columns_by_row=0)
    assert sheet.group_rows_by_column(0).to_dict() == {}
