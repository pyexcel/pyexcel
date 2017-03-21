from pyexcel.plugins import get_excel_formats, DB_SQL, DB_DJANGO


__pyexcel_plugins__ = [
    {
        'plugin_type': 'renderer',
        'submodule': 'database',
        'file_types': [DB_SQL, DB_DJANGO]
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
