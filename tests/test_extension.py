from nose.tools import raises


class TestExt:
    
    def test_test(self):
        """test test"""
        from pyexcel.ext import test
        from pyexcel.io import READERS
        from pyexcel.io import WRITERS
        assert READERS['test'] == 'test'
        assert WRITERS['test'] == 'test'

    @raises(ImportError)
    def test_unknown(self):
        """test unknown"""
        from pyexcel.ext import unknown
