import warnings

import pyexcel.ext.ods
import pyexcel.ext.xls
import pyexcel.ext.ods3
import pyexcel.ext.text
import pyexcel.ext.xlsx
from mock import patch

try:
    reload
except NameError:
    from imp import reload

EXPECTED_DEPRECATION_MESSAGE = (
    "Deprecated usage since v%s! "
    + "Explicit import is no longer required. pyexcel.ext.%s is auto imported."
)


@patch.object(warnings, "warn")
def test_ods_note(warn):
    reload(pyexcel.ext.ods)
    warn.assert_called_with(EXPECTED_DEPRECATION_MESSAGE % ("0.2.2", "ods"))


@patch.object(warnings, "warn")
def test_ods3_note(warn):
    reload(pyexcel.ext.ods3)
    warn.assert_called_with(EXPECTED_DEPRECATION_MESSAGE % ("0.2.2", "ods3"))


@patch.object(warnings, "warn")
def test_xls_note(warn):
    reload(pyexcel.ext.xls)
    warn.assert_called_with(EXPECTED_DEPRECATION_MESSAGE % ("0.2.2", "xls"))


@patch.object(warnings, "warn")
def test_xlsx_note(warn):
    reload(pyexcel.ext.xlsx)
    warn.assert_called_with(EXPECTED_DEPRECATION_MESSAGE % ("0.2.2", "xlsx"))


@patch.object(warnings, "warn")
def test_text_note(warn):
    reload(pyexcel.ext.text)
    warn.assert_called_with(EXPECTED_DEPRECATION_MESSAGE % ("0.2.1", "text"))
