import pytest
from pyexcel import Sheet
from pyexcel.internal.sheets._shared import excel_cell_position


@pytest.mark.parametrize(
    "reference",
    ["A0", "A00", "A1extra", "A1:B2", "A1\n", "A1 ", "1A", "A-1", ""],
)
def test_invalid_reference_cannot_read_or_overwrite_another_cell(reference):
    sheet = Sheet([[1, 2], [3, 4]])
    with pytest.raises(KeyError):
        sheet[reference]
    with pytest.raises(KeyError):
        sheet[reference] = 99
    assert sheet.to_array() == [[1, 2], [3, 4]]


@pytest.mark.parametrize(
    "reference, expected",
    [
        ("A1", (0, 0)),
        ("a1", (0, 0)),
        ("AA10", (9, 26)),
        ("aBc123", (122, 730)),
        ("A01", (0, 0)),
    ],
)
def test_complete_positive_references_keep_existing_coordinates(
    reference, expected
):
    assert excel_cell_position(reference) == expected


def test_valid_reference_can_expand_and_update_a_sheet():
    sheet = Sheet([[1]])
    sheet["B2"] = 99
    assert sheet["B2"] == 99
    assert sheet["A1"] == 1
