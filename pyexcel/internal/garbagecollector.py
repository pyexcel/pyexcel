"""
    pyexcel.internal.garbagecollector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Parsing excel sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
GARBAGE = []


def append(item):
    global GARBAGE
    GARBAGE.append(item)


def free_resource():
    for item in GARBAGE:
        item.close()
        item = None
    reset()


def reset():
    global GARBAGE
    GARBAGE = []
