from pyexcel import Reader
from pyexcel.utils import to_array
from pyexcel.formatters import SheetFormatter
from pyexcel.formatters import STRING_FORMAT

r=Reader("tutorial_datatype_02.ods")
to_array(r)

def cleanse_func(v, t):
    v = v.replace("&nbsp;", "")
    v = v.rstrip().strip()
    return v

sf = SheetFormatter(STRING_FORMAT, cleanse_func)
r.add_formatter(sf)
to_array(r)
