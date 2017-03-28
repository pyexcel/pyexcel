from pyexcel._compact import PY2


NO_COLUMN_NAMES = "Only sheet with column names is accepted"


def _set_dictionary_key(adict, sheet_name):
    if PY2:
        (old_sheet_name, array) = adict.items()[0]
    else:
        (old_sheet_name, array) = list(adict.items())[0]
    adict[sheet_name] = array
    adict.pop(old_sheet_name)
