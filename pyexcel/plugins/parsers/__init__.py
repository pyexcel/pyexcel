from pyexcel.plugins import get_excel_reader_formats, DB_SQL, DB_DJANGO


__pyexcel_plugins__ = [
    {
        'plugin_type': 'parser',
        'submodule': 'excel',
        'file_types': get_excel_reader_formats()
    },
    {
        'plugin_type': 'parser',
        'submodule': 'database',
        'file_types': [DB_SQL, DB_DJANGO]
    }
]
