"""
convert_xls_to_ods.py
:copyright: (c) 2014-2017 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows how to use **Book** to convert
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

you will need to install pyexcel-ods or pyexcel-ods3
depending on your python version

  pip install pyexcel-xls
  pip install pyexcel-ods3

"""
import os
import pyexcel as pe


def main(base_dir):
    # Simple open the file using Book
    pe.save_book_as(
        file_name=os.path.join(base_dir, "multiple-sheets.xls"),
        dest_file_name=os.path.join(base_dir, "multiple-sheets.xlsx")
    )


if __name__ == '__main__':
    main(os.getcwd())
