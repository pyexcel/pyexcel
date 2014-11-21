import sys

PY2 = sys.version_info[0] == 2
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

if PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO, StringIO