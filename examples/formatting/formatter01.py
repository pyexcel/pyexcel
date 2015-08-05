"""
pyexcel_server.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This file shows you how to use column format function
"""
import os
import pyexcel as pe


def main(base_dir):
    sheet = pe.load(os.path.join(base_dir,"tutorial_datatype_01.xls"), name_columns_by_row=0)
    print(sheet.to_dict())
    #{u'userid': [10120.0, 10121.0, 10122.0], u'name': [u'Adam', u'Bella', u'Cedar']}
    sheet.column.format(0, str)
    print(sheet.to_dict())
    #{u'userid': ['10120.0', '10121.0', '10122.0'], u'name': [u'Adam', u'Bella', u'Cedar']}



if __name__ == '__main__':
    main(os.getcwd())