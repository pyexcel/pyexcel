import sys

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

def is_array_type(an_array, atype):
    tmp = [ i for i in an_array if not isinstance(i, atype)]
    return len(tmp) == 0

