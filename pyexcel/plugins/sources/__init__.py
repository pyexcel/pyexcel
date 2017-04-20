"""
    pyexcel.plugins.sources
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A list of built-in sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.internal.common import PyexcelPluginList
from pyexcel.internal import PARSER, RENDERER

__pyexcel_plugins__ = PyexcelPluginList(__name__).add_a_source(
    submodule='http',
    fields=['url'],
    targets=['sheet', 'book'],
    actions=['read'],
    attributes=['url'],
    key='url'
).add_a_source(
    submodule='file_input',
    fields=['file_name'],
    targets=['sheet', 'book'],
    attributes=[],
    actions=['read'],
).add_a_source(
    submodule='memory_input',
    fields=['file_type'],
    targets=['sheet', 'book'],
    actions=['read'],
    key='file_type',
    attributes=PARSER.get_all_file_types
).add_a_source(
    submodule='file_output',
    fields=['file_name'],
    targets=['sheet', 'book'],
    attributes=[],
    actions=['write'],
).add_a_source(
    submodule='output_to_memory',
    fields=['file_type'],
    targets=['sheet', 'book'],
    actions=['write'],
    key='file_type',
    attributes=RENDERER.get_all_file_types,
).add_a_source(
    submodule='pydata.bookdict',
    fields=['bookdict'],
    targets=['sheet', 'book'],
    actions=['write', 'read'],
    key='bookdict',
    attributes=['bookdict']
).add_a_source(
    submodule='pydata.dictsource',
    fields=['adict'],
    targets=['sheet', 'book'],
    actions=['write', 'read'],
    key='adict',
    attributes=['dict'],
).add_a_source(
    submodule='pydata.arraysource',
    fields=['array'],
    targets=['sheet', 'book'],
    actions=['write', 'read'],
    key='array',
    attributes=['array'],
).add_a_source(
    submodule='pydata.records',
    fields=['records'],
    targets=['sheet', 'book'],
    actions=['write', 'read'],
    key='records',
    attributes=['records'],
).add_a_source(
    submodule='django',
    fields=['model'],
    targets=['sheet'],
    actions=['write', 'read'],
).add_a_source(
    submodule='django',
    fields=['models'],
    targets=['book'],
    actions=['write', 'read'],
).add_a_source(
    submodule='sqlalchemy',
    fields=['session', 'table'],
    targets=['sheet'],
    actions=['write', 'read'],
).add_a_source(
    submodule='sqlalchemy',
    fields=['session', 'tables'],
    targets=['book'],
    actions=['write', 'read'],
).add_a_source(
    submodule='querysets',
    fields=['column_names', 'query_sets'],
    targets=['sheet'],
    actions=['read'],
)
