"""
formatter02.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This example shows you how to use custom formatter function

"""
import pyexcel as pe
from pyexcel.ext import ods3

sheet = pe.load("tutorial_datatype_02.ods")
print(sheet.to_array())

def cleanse_func(v):
    v = v.replace("&nbsp;", "")
    v = v.rstrip().strip()
    return v

sf = pe.SheetFormatter(cleanse_func)
sheet.add_formatter(sf)
print(sheet.to_array())
