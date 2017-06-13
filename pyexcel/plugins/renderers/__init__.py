"""
    pyexcel.plugins.renderers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A list of built-in renderers

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.plugins import WRITERS
from pyexcel_io.constants import DB_SQL, DB_DJANGO

from pyexcel.plugins import PyexcelPluginChain


PyexcelPluginChain(__name__).add_a_renderer(
    relative_plugin_class_path='sqlalchemy.SQLAlchemyRenderer',
    file_types=[DB_SQL]
).add_a_renderer(
    relative_plugin_class_path='django.DjangoRenderer',
    file_types=[DB_DJANGO]
).add_a_renderer(
    relative_plugin_class_path='excel.ExcelRenderer',
    file_types=WRITERS.get_all_formats()
).add_a_renderer(
    relative_plugin_class_path='_texttable.TextTableRenderer',
    file_types=['texttable']
)
