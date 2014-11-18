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


    def test_tabulate(self):
        import pyexcel as pe
        from pyexcel.ext import presentation
        a = [[1,1]]
        m = pe.sheets.Matrix(a)
        print(str(m))
        assert str(m) == "pyexcel.sheets.matrix.Matrix"
