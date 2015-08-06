"""
convert_xls_to_ods2.py
:copyright: (c) 2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows how to use **pyexcel.save_book_as** to convert
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
import os
import pyexcel as pe
# you will need to install pyexcel-ods or pyexcel-ods3
# depending on your python version
import pyexcel.ext.xls
import pyexcel.ext.ods3

def main(base_dir):
    # Simple open the file using Book
    pe.save_book_as(file_name=os.path.join(base_dir, "multiple-sheets.xls"),
                    dest_file_name="multiple-sheets.ods")
    
    # then you will have the book in ods

if __name__ == '__main__':
    main(os.getcwd())
