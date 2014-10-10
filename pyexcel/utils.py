from .sheets import Sheet

def dict_to_array(the_dict, with_keys=True):
    content = []
    keys = sorted(the_dict.keys())
    if with_keys:
        content.append(keys)
    max_length = -1
    for k in keys:
        column_length = len(the_dict[k])
        if max_length == -1:
            max_length = column_length
        elif max_length < column_length:
            max_length = column_length
    for i in range(0, max_length):
        row_data = []
        for k in keys:
            if i < len(the_dict[k]):
                row_data.append(the_dict[k][i])
            else:
                row_data.append('')
        content.append(row_data)
    return content


def transpose(in_array):
    max_length = -1
    new_array = []
    for c in in_array:
        column_length = len(c)
        if max_length == -1:
            max_length = column_length
        elif max_length < column_length:
            max_length = column_length
    for i in range(0, max_length):
        row_data = []
        for c in in_array:
            if i < len(c):
                row_data.append(c[i])
            else:
                row_data.append('')
        new_array.append(row_data)
    return new_array


def to_array(o):
    """convert a reader iterator to an array"""
    array = []
    for i in o:
        array.append(i)
    return array


def to_dict(o):
    """convert a reader iterator to a dictionary"""
    the_dict = {}
    series = "Series_%d"
    count = 1
    for c in o:
        if type(c) == dict:
            the_dict.update(c)
        elif isinstance(c, Sheet):
            the_dict.update({c.name: to_array(c)})
        else:
            key = series % count
            the_dict.update({key: c})
            count += 1
    return the_dict


def to_records(reader):
    """
    Make an array of dictionaries

    It takes the first row as keys and the rest of
    the rows as values. Then zips keys and row values
    per each row. This is particularly helpful for
    database operations.
    """
    if isinstance(reader, Sheet) is False:
        raise NotImplementedError
    headers = reader.series()
    need_revert = False
    if len(headers) == 0:
        reader.become_series()
        headers = reader.series()
        need_revert = True
    ret = []
    for row in reader.rows():
        the_dict = dict(zip(headers, row))
        ret.append(the_dict)

    if need_revert:
        reader.become_sheet()
    return ret


def to_one_dimensional_array(iterator):
    """convert a reader to one dimensional array"""
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array
