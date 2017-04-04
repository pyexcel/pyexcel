from pyexcel.internal import parser, renderer

__pyexcel_plugins__ = [
    {
        'plugin_type': 'source',
        'submodule': 'http',
        'fields': ['url'],
        'targets': ['sheet', 'book'],
        'actions': ['read'],
        'attributes': ['url'],
        'key': 'url'
    },
    {
        'plugin_type': 'source',
        'submodule': 'file_input',
        'fields': ['file_name'],
        'targets': ['sheet', 'book'],
        'attributes': [],
        'actions': ['read'],
    },
    {
        'plugin_type': 'source',
        'submodule': 'memory_input',
        'fields': ['file_type'],
        'targets': ['sheet', 'book'],
        'actions': ['read'],
        'key': 'file_type',
        'attributes': parser.get_all_file_types
    },
    {
        'plugin_type': 'source',
        'submodule': 'file_output',
        'fields': ['file_name'],
        'targets': ['sheet', 'book'],
        'attributes': [],
        'actions': ['write'],
    },
    {
        'plugin_type': 'source',
        'submodule': 'output_to_memory',
        'fields': ['file_type'],
        'targets': ['sheet', 'book'],
        'actions': ['write'],
        'key': 'file_type',
        'attributes': renderer.get_all_file_types
    },
    {
        'plugin_type': 'source',
        'submodule': 'pydata',
        'fields': ['bookdict'],
        'targets': ['sheet', 'book'],
        'actions': ['write', 'read'],
        'key': 'bookdict',
        'attributes': ['bookdict']
    },
    {
        'plugin_type': 'source',
        'submodule': 'pydata',
        'fields': ['adict'],
        'targets': ['sheet', 'book'],
        'actions': ['write', 'read'],
        'key': 'adict',
        'attributes': ['dict']
    },
    {
        'plugin_type': 'source',
        'submodule': 'pydata',
        'fields': ['array'],
        'targets': ['sheet', 'book'],
        'actions': ['write', 'read'],
        'key': 'array',
        'attributes': ['array']
    },
    {
        'plugin_type': 'source',
        'submodule': 'pydata',
        'fields': ['records'],
        'targets': ['sheet', 'book'],
        'actions': ['write', 'read'],
        'key': 'records',
        'attributes': ['records']
    },
    {
        'plugin_type': 'source',
        'submodule': 'django',
        'fields': ['model'],
        'targets': ['sheet'],
        'actions': ['write', 'read'],
        'key': None,
        'attributes': []
    },
    {
        'plugin_type': 'source',
        'submodule': 'django',
        'fields': ['models'],
        'targets': ['book'],
        'actions': ['write', 'read'],
        'key': None,
        'attributes': []
    },
    {
        'plugin_type': 'source',
        'submodule': 'sqlalchemy',
        'fields': ['session', 'table'],
        'targets': ['sheet'],
        'actions': ['write', 'read'],
        'key': None,
        'attributes': []
    },
    {
        'plugin_type': 'source',
        'submodule': 'sqlalchemy',
        'fields': ['session', 'tables'],
        'targets': ['book'],
        'actions': ['write', 'read'],
        'key': None,
        'attributes': []
    },
    {
        'plugin_type': 'source',
        'submodule': 'querysets',
        'fields': ['column_names', 'query_sets'],
        'targets': ['sheet'],
        'actions': ['read'],
        'key': None,
        'attributes': []
    }
]
