import json

def to_json(iterator):
    array = []
    for i in iterator:
        array.append(i)
    return json.dumps(array)

def to_array(iterator):
    array = []
    for i in iterator:
        array.append(i)
    return array

def to_one_dimensional_array(iterator):
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array    