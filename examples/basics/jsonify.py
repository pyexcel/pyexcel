"""
jsonify.py
:copyright: (c) 2014-2025 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details


You will need pyexcel-text for json output

"""
import os

import pyexcel as pe


def main(base_dir):
    # "example.xls","example.xlsx","example.ods", "example.xlsm"
    sheet = pe.get_sheet(file_name=os.path.join(base_dir,
                                                "example.csv"))
    print(sheet.json)


if __name__ == '__main__':
    main(os.getcwd())
