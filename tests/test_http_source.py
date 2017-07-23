from unittest import TestCase
from mock import patch, MagicMock
import pyexcel as pe
from textwrap import dedent
from pyexcel._compact import PY2


class TestHttpBookSource(TestCase):
    def setUp(self):
        self.patcher = patch('pyexcel._compact.request.urlopen')
        mock_open = self.patcher.start()
        m = MagicMock()
        self.mocked_info = MagicMock()
        m.info.return_value = self.mocked_info
        m.read.return_value = "1,2,3"
        mock_open.return_value = m

    def tearDown(self):
        self.patcher.stop()

    def test_url_source_via_content_type(self):
        book = pe.get_book(url="xx.csv")
        if PY2:
            self.mocked_info.type.return_value = "text/csv"
        else:
            self.mocked_info.get_content_type.return_value = "text/csv"
        content = dedent("""
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""").strip('\n')
        self.assertEqual(str(book), content)

    def test_url_source_via_file_suffix(self):
        book = pe.get_book(url="xx.csv")
        content = dedent("""
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""").strip('\n')
        self.assertEqual(str(book), content)

    def test_url_source_via_file_suffix_get_sheet(self):
        sheet = pe.get_sheet(url="xx.csv")
        content = dedent("""
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""").strip('\n')
        self.assertEqual(str(sheet), content)
