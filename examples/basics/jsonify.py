"""
jsonify.py
:copyright: (c) 2014-2017 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details
"""
import os
import pyexcel as pe
import json


def main(base_dir):
    # "example.xls","example.xlsx","example.ods", "example.xlsm"
    sheet = pe.get_sheet(file_name=os.path.join(base_dir,
                                                "example.csv"))
    print(json.dumps(sheet.to_array()))


if __name__ == '__main__':
    main(os.getcwd())
