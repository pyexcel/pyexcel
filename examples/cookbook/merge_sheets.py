"""
pyexcel_server.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This code snippet shows you how to merge files that are scattered in
a directory into one excel book

"""
import pyexcel as pe
import pyexcel.ext.xls
import glob
import os

merged = pe.Book()
for file in glob.glob(os.path.join("scattered-csv-files","*.csv")):
    merged += pe.load(file)
merged.save_as("merged.xls")
