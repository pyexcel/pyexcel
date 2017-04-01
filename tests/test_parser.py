from pyexcel.parser import Parser
from nose.tools import raises


@raises(NotImplementedError)
def test_default_parser():
    parser = Parser('xls')
    parser.parse_file('afile.xls')


@raises(NotImplementedError)
def test_default_parser_2():
    parser = Parser('xls')
    parser.parse_file_stream('afile xls stream')


@raises(NotImplementedError)
def test_default_parser_3():
    parser = Parser('xls')
    parser.parse_file_content('afile content')
