from pyexcel_io.plugins import iomanager
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
        'file_types': iomanager.get_all_writer_formats()
    },
    {
        'plugin_type': 'renderer',
        'submodule': '_texttable',
        'file_types': ['texttable']
    }
]
