class TestExt:
    def test(self):
        from pyexcel.ext import test
        from pyexcel.io import READERS
        from pyexcel.io import WRITERS
        assert READERS['test'] == 'test'
        assert WRITERS['test'] == 'test'