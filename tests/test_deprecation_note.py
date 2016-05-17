from unittest import TestCase
from mock import patch
from _compact import StringIO
import pyexcel.ext.ods
import pyexcel.ext.ods3
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import pyexcel.ext.text


try:
    reload
except NameError:
    from imp import reload


EXPECTED_DEPRECATION_MESSAGE = (
    'Deprecated usage since v%s! '+
    'Explicit import is no longer required. pyexcel.ext.%s is auto imported.\n'
)


class TestNote(TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_ods_note(self, stdout):
        reload(pyexcel.ext.ods)
        self.assertEqual(stdout.getvalue(), EXPECTED_DEPRECATION_MESSAGE % ('0.2.2', 'ods'))

    @patch('sys.stdout', new_callable=StringIO)
    def test_xls_note(self, stdout):
        reload(pyexcel.ext.xls)
        self.assertEqual(stdout.getvalue(), EXPECTED_DEPRECATION_MESSAGE % ('0.2.2', 'xls'))

    @patch('sys.stdout', new_callable=StringIO)
    def test_xlsx_note(self, stdout):
        reload(pyexcel.ext.xlsx)
        self.assertEqual(stdout.getvalue(), EXPECTED_DEPRECATION_MESSAGE % ('0.2.2', 'xlsx'))

    @patch('sys.stdout', new_callable=StringIO)
    def test_ods3_note(self, stdout):
        reload(pyexcel.ext.ods3)
        self.assertEqual(stdout.getvalue(), EXPECTED_DEPRECATION_MESSAGE % ('0.2.2', 'ods3'))

    @patch('sys.stdout', new_callable=StringIO)
    def test_text_note(self, stdout):
        reload(pyexcel.ext.text)
        self.assertEqual(stdout.getvalue(), EXPECTED_DEPRECATION_MESSAGE % ('0.2.1', 'text'))
