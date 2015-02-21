"""
pyexcel_server.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This example shows you how to use custom formatter function

"""
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
