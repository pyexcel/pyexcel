"""
    pyexcel.plugins.renderers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A list of built-in renderers

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.plugins import writers
from pyexcel_io.constants import DB_SQL, DB_DJANGO


__pyexcel_plugins__ = [
    {
        'plugin_type': 'renderer',
        'submodule': 'sqlalchemy',
        'file_types': [DB_SQL]
    },
    {
        'plugin_type': 'renderer',
        'submodule': 'django',
        'file_types': [DB_DJANGO]
    },
    {
        'plugin_type': 'renderer',
        'submodule': 'excel',
        'file_types': writers.get_all_formats()
    },
    {
        'plugin_type': 'renderer',
        'submodule': '_texttable',
        'file_types': ['texttable']
    }
]
