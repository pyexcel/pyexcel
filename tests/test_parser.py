from pyexcel.parser import AbstractParser, DbParser
from nose.tools import raises


@raises(NotImplementedError)
def test_default_parser():
    parser = AbstractParser("xls")
    parser.parse_file("afile.xls")


@raises(NotImplementedError)
def test_default_parser_2():
    parser = AbstractParser("xls")
    parser.parse_file_stream("afile xls stream")


@raises(NotImplementedError)
def test_default_parser_3():
    parser = AbstractParser("xls")
    parser.parse_file_content("afile content")


@raises(Exception)
def test_dbparser():
    parser = DbParser("sql")
    parser.parse_file("some name")


@raises(Exception)
def test_dbparser_1():
    parser = DbParser("sql")
    parser.parse_file_content("some content")


@raises(NotImplementedError)
def test_dbparser_2():
    parser = DbParser("sql")
    parser.parse_db("some name")
