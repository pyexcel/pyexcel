"""
    pyexcel.utils
    ~~~~~~~~~~~~~~~~~~~

    Utility functions for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""


def to_array(iterator):
    """convert a reader iterator to an array"""
    array = []
    for i in iterator:
        array.append(i)
    return array


def to_dict(iterator):
    """convert a reader iterator to a dictionary"""
    the_dict = {}
    series = "Series_%d"
    count = 1
    for c in iterator:
        if type(c) == dict:
            the_dict.update(c)
        else:
            key = series % count
            the_dict.update({key: c})
            count += 1
    return the_dict


def to_one_dimensional_array(iterator):
    """convert a reader to one dimensional array"""
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array
