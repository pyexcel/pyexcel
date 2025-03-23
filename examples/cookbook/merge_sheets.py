"""
merge_sheets.py
:copyright: (c) 2014-2025 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This code snippet shows you how to merge files that are scattered in
a directory into one excel book

Please install pyexcel-xls
"""
import os
import glob

import pyexcel as pe


def main(base_dir):
    merged = pe.Book()
    files = glob.glob(os.path.join(base_dir, "scattered-csv-files", "*.csv"))
    for csv_file in files:
        merged += pe.load(csv_file)
    merged.save_as("merged.xls")


if __name__ == '__main__':
    main(os.getcwd())
