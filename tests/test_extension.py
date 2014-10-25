class TestExt:
    
    def test_test(self):
        """test test"""
        from pyexcel.ext import test
        from pyexcel.io import READERS
        from pyexcel.io import WRITERS
        assert READERS['test'] == 'test'
        assert WRITERS['test'] == 'test'
        
    def test_unknown(self):
        """test unknown"""
        try:
            from pyexcel.ext import unknown
            assert 1==2
        except ImportError:
            assert 1==1
