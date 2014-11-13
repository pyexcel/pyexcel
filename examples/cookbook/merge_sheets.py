"""
pyexcel_server.py
:copyright: (c) 2014 by C. W.
:license: GPL v3

This code snippet shows you how to merge files that are scattered in
a directory into one excel book

"""
import pyexcel as pe
import glob

merged = pe.Book()
for file in glob.glob("*.csv"):
    merged += pe.load(file)
merged.save_as("merged.ods")