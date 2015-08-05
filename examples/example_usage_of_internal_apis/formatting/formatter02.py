"""
formatter01.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details
"""
import os
from pyexcel import Reader
from pyexcel.utils import to_array
from pyexcel.formatters import SheetFormatter
import pyexcel.ext.ods3


def main(base_dir):
    r=Reader(os.path.join(base_dir, "tutorial_datatype_02.ods"))
    to_array(r)
    
    def cleanse_func(v):
        v = v.replace("&nbsp;", "")
        v = v.rstrip().strip()
        return v
    
    sf = SheetFormatter(cleanse_func)
    r.add_formatter(sf)
    to_array(r)


if __name__ == '__main__':
    main(os.getcwd())