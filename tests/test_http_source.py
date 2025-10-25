from textwrap import dedent
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pyexcel as pe
from pyexcel._compact import BytesIO


class TestHttpBookSource(TestCase):
    def setUp(self):
        self.patcher = patch("pyexcel._compact.request.urlopen")
        mock_open = self.patcher.start()
        self.mocked_info = MagicMock()
        io = BytesIO("1,2,3".encode("utf-8"))
        io.info = self.mocked_info
        mock_open.return_value = io

    def tearDown(self):
        self.patcher.stop()

    def test_url_source_via_content_type(self):
        book = pe.get_book(url="xx.csv")
        self.mocked_info.get_content_type.return_value = "text/csv"
        content = dedent(
            """
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""",
        ).strip("\n")
        self.assertEqual(str(book), content)

    def test_url_source_via_file_suffix(self):
        book = pe.get_book(url="xx.csv")
        content = dedent(
            """
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""",
        ).strip("\n")
        self.assertEqual(str(book), content)

    def test_url_source_via_file_suffix_get_sheet(self):
        sheet = pe.get_sheet(url="xx.csv")
        content = dedent(
            """
        csv:
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+""",
        ).strip("\n")
        self.assertEqual(str(sheet), content)
