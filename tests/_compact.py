import sys

PY2 = sys.version_info[0] == 2
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

if PY2:
    from StringIO import StringIO
    from StringIO import StringIO as BytesIO
    execfile = execfile
else:
    from io import BytesIO, StringIO
    def execfile(filename, globals=None, locals=None):
        if globals is None:
            globals = sys._getframe(1).f_globals
        if locals is None:
            locals = sys._getframe(1).f_locals
        with open(filename, "r") as fh:
            exec(fh.read()+"\n", globals, locals)