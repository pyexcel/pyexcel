"""
    pyexcel.plugins.parsers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A list of built-in parsers

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.plugins import iomanager
from pyexcel_io.constants import DB_SQL, DB_DJANGO


__pyexcel_plugins__ = [
    {
        'plugin_type': 'parser',
        'submodule': 'excel',
        'file_types': iomanager.get_all_reader_formats()
    },
    {
        'plugin_type': 'parser',
        'submodule': 'sqlalchemy',
        'file_types': [DB_SQL]
    },
    {
        'plugin_type': 'parser',
        'submodule': 'django',
        'file_types': [DB_DJANGO]
    }
]
