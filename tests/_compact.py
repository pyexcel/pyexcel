# flake8: noqa
import sys

PY2 = sys.version_info[0] == 2
from collections import OrderedDict

if PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO, StringIO
