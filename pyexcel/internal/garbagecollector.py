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
