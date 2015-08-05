"""
jsonify.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details
"""
import os
from pyexcel import Reader
from pyexcel.utils import to_array
import json

def main(base_dir):
    # "example.xls","example.xlsx","example.ods", "example.xlsm"
    reader = Reader(os.path.join(base_dir,"example.csv"))
    data = to_array(reader.rows())
    print(json.dumps(data))

if __name__ == '__main__':
    main(os.getcwd())