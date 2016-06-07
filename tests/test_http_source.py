from unittest import TestCase
from mock import patch, MagicMock
import pyexcel as pe
from textwrap import dedent


class TestHttpBookSource(TestCase):
    @patch('pyexcel._compact.request.urlopen')
    def test_url_source_via_content_type(self, mock_open):
        m = MagicMock()
        x = MagicMock()
        x.type.return_value = "text/csv"
        m.info.return_value = x
        m.read.return_value = "1,2,3"
        mock_open.return_value = m
        book = pe.get_book(url="xx.csv")
        content = dedent("""
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""").strip('\n')
        self.assertEqual(str(book), content)

    @patch('pyexcel._compact.request.urlopen')
    def test_url_source_via_file_suffix(self, mock_open):
        m = MagicMock()
        x = MagicMock()
        x.type.return_value = "text"
        m.info.return_value = x
        m.read.return_value = "1,2,3"
        mock_open.return_value = m
        book = pe.get_book(url="xx.csv")
        content = dedent("""
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""").strip('\n')
        self.assertEqual(str(book), content)

    @patch('pyexcel._compact.request.urlopen')
    def test_url_source_via_file_suffix_get_sheet(self, mock_open):
        m = MagicMock()
        x = MagicMock()
        x.type.return_value = "text"
        m.info.return_value = x
        m.read.return_value = "1,2,3"
        mock_open.return_value = m
        sheet = pe.get_sheet(url="xx.csv")
        content = dedent("""
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""").strip('\n')
        self.assertEqual(str(sheet), content)
