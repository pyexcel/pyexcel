import os
import threading
from io import StringIO

from pyexcel import iget_array
from pyexcel.internal import garbagecollector as gc

from .nose_tools import eq_


def test_gc():
    gc.free_resources()
    data = iget_array(
        file_name=os.path.join("tests", "fixtures", "bug_01.csv"),
    )
    data = list(data)
    eq_(len(gc.GARBAGE), 1)
    gc.free_resources()
    assert len(gc.GARBAGE) == 0


def test_gc_custom():
    gc.free_resources()
    f = open(
        os.path.join("tests", "fixtures", "bug_01.csv"), "r", encoding="utf-8"
    )
    gc.append(f)
    eq_(len(gc.GARBAGE), 1)
    gc.free_resources()
    assert len(gc.GARBAGE) == 0


def test_gc_is_thread_local():
    gc.free_resources()
    ready = [threading.Event(), threading.Event()]
    first_done = threading.Event()
    failures = []

    def worker(index):
        try:
            handle = StringIO("data")
            gc.append(handle)
            eq_(len(gc.GARBAGE), 1)
            ready[index].set()
            ready[1 - index].wait(timeout=5)
            if index == 0:
                gc.free_resources()
                assert handle.closed
                first_done.set()
            else:
                first_done.wait(timeout=5)
                assert not handle.closed
                gc.free_resources()
                assert handle.closed
            assert len(gc.GARBAGE) == 0
        except Exception as exc:
            failures.append(exc)

    first = threading.Thread(target=worker, args=(0,))
    second = threading.Thread(target=worker, args=(1,))
    first.start()
    second.start()
    first.join()
    second.join()

    assert not failures
    assert len(gc.GARBAGE) == 0
