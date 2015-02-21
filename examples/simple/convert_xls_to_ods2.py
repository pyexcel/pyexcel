"""
convert_xls_to_ods2.py
:copyright: (c) 2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows how to use **pyexcel.save_as** and **BookWriter** class to convert
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
pe.save_as(file_name="multiple-sheets.xls",
           out_file="multiple-sheets.ods")

# then you will have the book in ods