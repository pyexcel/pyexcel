"""
convert_xls_to_ods_one_liner.py
:copyright: (c) 2015 by C. W.
:license: GPL v3

This shows how to use pyexcel.save_book_as function to convert
xls file to ods file.

What this example implies is that you can do the conversion in
between these formats:
==== === === === === ==== ====
     ods csv tsv xls xlsx xlsm
==== === === === === ==== ====
ods  y   y   y   y   y    y
tsv  y   y   y   y   y    y
csv  y   y   y   y   y    y   
xls  y   y   y   y   y    y   
xlsx y   y   y   y   y    y   
xlsm y   y   y   y   y    y   
---- --- --- --- --- ---- ----
"""
import pyexcel as pe
# you will need to install pyexcel-ods or pyexcel-ods3
# depending on your python version
import pyexcel.ext.xls
import pyexcel.ext.ods

# Simple open the file using Book
pe.save_book_as(
    file_name="multiple-sheets.xls", # incoming file
    out_file="multiple-sheets.ods" # outgoing file
)

# then you will have the book in ods