import json


def to_array(iterator):
    array = []
    for i in iterator:
        array.append(i)
    return array


def to_dict(iterator):
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
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array
