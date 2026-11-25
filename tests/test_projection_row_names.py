import pytest
from pyexcel import Sheet


@pytest.mark.parametrize("exclusion", [False, True])
@pytest.mark.parametrize("names_from_data", [False, True])
def test_projection_preserves_named_row_access(exclusion, names_from_data):
    if names_from_data:
        sheet = Sheet(
            [["", "a", "b"], ["first", 1, 2], ["second", 3, 4]],
            name_columns_by_row=0,
            name_rows_by_column=0,
            name="source",
        )
    else:
        sheet = Sheet(
            [[1, 2], [3, 4]],
            colnames=["a", "b"],
            rownames=["first", "second"],
            name="source",
        )
    projected = sheet.project(["a"] if exclusion else ["b"], exclusion)
    assert projected.rownames == ["first", "second"]
    assert projected["second", "b"] == 4
    assert projected.to_array() == [["", "b"], ["first", 2], ["second", 4]]
    assert projected.name == "source"
    projected.rownames[0] = "changed"
    assert sheet.rownames == ["first", "second"]
