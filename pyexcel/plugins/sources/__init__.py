from pyexcel.parsers import get_all_file_types as get_parser_file_types
from pyexcel.renderers import get_all_file_types as get_renderer_file_types

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
        'attributes': get_parser_file_types
    },
    {
        'plugin_type': 'source',
        'submodule': 'file_outputput',
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
        'attributes': get_renderer_file_types
    }
]
