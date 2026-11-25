import pytest
from pyexcel import Sheet


@pytest.mark.parametrize(
    "data", [[[1]], [[1, 2, 3]], [[1], [2], [3]], [[1, 2], [3, 4], [5, 6]]]
)
@pytest.mark.parametrize("axis", ["row", "column"])
@pytest.mark.parametrize("method_access", [False, True])
def test_negative_indices_match_positive_indices(data, axis, method_access):
    sheet = Sheet(data)
    accessor = getattr(sheet, axis)
    size = len(data) if axis == "row" else len(data[0])
    for positive in range(size):
        if method_access:
            read = getattr(sheet, axis + "_at")
            assert read(positive - size) == read(positive)
        else:
            assert accessor[positive - size] == accessor[positive]


@pytest.mark.parametrize("axis", ["row", "column"])
def test_negative_index_outside_axis_still_raises(axis):
    sheet = Sheet([[1, 2], [3, 4]])
    with pytest.raises(IndexError):
        getattr(sheet, axis)[-3]


@pytest.mark.parametrize("axis", ["row", "column"])
def test_negative_index_on_empty_sheet_still_raises(axis):
    with pytest.raises(IndexError):
        getattr(Sheet(), axis)[-1]


def test_first_row_selected_by_negative_index_remains_a_copy():
    sheet = Sheet([[1, 2], [3, 4]])
    row = sheet.row[-2]
    row[0] = 99
    assert sheet.row[0] == [1, 2]
