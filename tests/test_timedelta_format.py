import datetime

import pytest
from pyexcel import Sheet
from pyexcel.internal.sheets.formatters import to_format


@pytest.mark.parametrize(
    "value, expected",
    [
        (datetime.timedelta(hours=25), "1 day, 1:00:00"),
        (datetime.timedelta(0), "0:00:00"),
        (datetime.timedelta(hours=-1), "-1 day, 23:00:00"),
        (datetime.timedelta(microseconds=1), "0:00:00.000001"),
        (datetime.timedelta(microseconds=-1), "-1 day, 23:59:59.999999"),
    ],
)
def test_timedelta_string_and_sheet_display(value, expected):
    assert to_format(str, value) == expected
    sheet = Sheet([["Duration"], [value]])
    assert expected in str(sheet)
    assert sheet[1, 0] == value


@pytest.mark.parametrize("target", [int, float, bool, datetime.datetime])
def test_timedelta_non_string_targets_still_raise(target):
    with pytest.raises(TypeError, match="timedelta.*not JSON serializable"):
        to_format(target, datetime.timedelta(hours=25))


@pytest.mark.parametrize(
    "value, expected",
    [
        (datetime.date(2026, 9, 12), "12/09/26"),
        (datetime.datetime(2026, 9, 12, 13, 14, 15), "12/09/26"),
        (datetime.time(23, 1, 2), "23:01:02"),
    ],
)
def test_existing_date_and_time_strings(value, expected):
    assert to_format(str, value) == expected


def test_other_unknown_types_keep_json_behavior():
    assert to_format(str, {"duration": 25}) == '{"duration": 25}'
    with pytest.raises(TypeError, match="not JSON serializable"):
        to_format(str, object())
