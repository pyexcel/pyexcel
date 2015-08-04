"""
pyexcel_server.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This file shows you how to use column format function
"""
import pyexcel as pe

sheet = pe.load("tutorial_datatype_01.xls", name_columns_by_row=0)
print(sheet.to_dict())
#{u'userid': [10120.0, 10121.0, 10122.0], u'name': [u'Adam', u'Bella', u'Cedar']}
sheet.column.format(0, str)
print(sheet.to_dict())
#{u'userid': ['10120.0', '10121.0', '10122.0'], u'name': [u'Adam', u'Bella', u'Cedar']}