import pyexcel as pe
from pyexcel.ext import ods

sheet = pe.load("tutorial_datatype_02.ods")
print(sheet.to_array())

def cleanse_func(v, t):
    v = v.replace("&nbsp;", "")
    v = v.rstrip().strip()
    return v

sf = pe.SheetFormatter(str, cleanse_func)
sheet.add_formatter(sf)
print(sheet.to_array())
