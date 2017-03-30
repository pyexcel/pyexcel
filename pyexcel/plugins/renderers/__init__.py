from pyexcel.plugins import get_excel_formats, DB_SQL, DB_DJANGO


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
        'file_types': get_excel_formats()
    },
    {
        'plugin_type': 'renderer',
        'submodule': '_texttable',
        'file_types': ['texttable']
    }
]
