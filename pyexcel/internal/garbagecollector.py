"""
    pyexcel.internal.garbagecollector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Simple garbage collector

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import append_doc
import pyexcel.docstrings as docs


GARBAGE = []


def append(item):
    global GARBAGE
    GARBAGE.append(item)


@append_doc(docs.FREE_RESOURCES)
def free_resources():
    """
    Close file handles opened by signature functions that starts with 'i'
    """
    for item in GARBAGE:
        item.close()
        item = None
    reset()


def reset():
    global GARBAGE
    GARBAGE = []
