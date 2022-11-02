import os
from nose.tools import eq_
from pyexcel import iget_array
from pyexcel.internal import garbagecollector as gc

def test_gc():
    gc.free_resources()
    data = iget_array(
        file_name=os.path.join("tests", "fixtures", "bug_01.csv")
    )
    data = list(data)
    eq_(len(gc.GARBAGE), 1)
    gc.free_resources()
    assert len(gc.GARBAGE) == 0


def test_gc_custom():
    gc.free_resources()
    f = open(os.path.join("tests", "fixtures", "bug_01.csv"), "r", encoding="utf-8")
    gc.append(f)
    eq_(len(gc.GARBAGE), 1)
    gc.free_resources()
    assert len(gc.GARBAGE) == 0
