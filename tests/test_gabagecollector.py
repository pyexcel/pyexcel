import os
from nose.tools import eq_
import pyexcel.internal.garbagecollector as gc
from pyexcel import iget_array


def test_gc():
    gc.free_resource()
    data = iget_array(file_name=os.path.join("tests",
                                             "fixtures", "bug_01.csv"))
    data = list(data)
    eq_(len(gc.GARBAGE), 1)
    gc.free_resource()
    assert len(gc.GARBAGE) == 0


def test_gc_custom():
    gc.free_resource()
    f = open(os.path.join("tests", "fixtures", "bug_01.csv"), 'r')
    gc.append(f)
    eq_(len(gc.GARBAGE), 1)
    gc.free_resource()
    assert len(gc.GARBAGE) == 0
