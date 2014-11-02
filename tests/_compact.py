import six
import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
if six.PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO, StringIO