"""
formatter02.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This example shows you how to use custom formatter function

Please install pyexcel-ods3
"""
import os
import pyexcel as pe


def main(base_dir):
    sheet = pe.load(os.path.join(base_dir, "tutorial_datatype_02.xls"))
    print(sheet.array)

    def cleanse_func(v):
        v = v.replace("&nbsp;", "")
        v = v.rstrip().strip()
        return v

    sheet.map(cleanse_func)
    print(sheet.array)


if __name__ == '__main__':
    main(os.getcwd())
