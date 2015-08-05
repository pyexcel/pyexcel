"""
formatter01.py
:copyright: (c) 2014-2015 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details
"""
import os
from pyexcel import SeriesReader
from pyexcel.utils import to_dict
from pyexcel.formatters import ColumnFormatter
import pyexcel.ext.xls

def main(base_dir):
    reader = SeriesReader(os.path.join(base_dir, "tutorial_datatype_01.xls"))
    print(to_dict(reader))
    #{u'userid': [10120.0, 10121.0, 10122.0], u'name': [u'Adam', u'Bella', u'Cedar']}
    formatter = ColumnFormatter(0, str)
    reader.add_formatter(formatter)
    to_dict(reader)
    #{u'userid': ['10120.0', '10121.0', '10122.0'], u'name': [u'Adam', u'Bella', u'Cedar']}

if __name__ == '__main__':
    main(os.getcwd())