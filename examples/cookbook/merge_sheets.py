"""
merge_sheets.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This code snippet shows you how to merge files that are scattered in
a directory into one excel book

Please install pyexcel-xls
"""
import pyexcel as pe
import glob
import os


def main(base_dir):
    merged = pe.Book()
    for file in glob.glob(os.path.join(base_dir, "scattered-csv-files","*.csv")):
        merged += pe.load(file)
    merged.save_as("merged.xls")


if __name__ == '__main__':
    main(os.getcwd())
