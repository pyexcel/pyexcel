"""
    pyexcel.plugins.renderers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A list of built-in renderers

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.plugins import writers
from pyexcel_io.constants import DB_SQL, DB_DJANGO

from pyexcel.internal.common import PyexcelPluginList


PyexcelPluginList(__name__).add_a_renderer(
    submodule='sqlalchemy.SQLAlchemyRenderer',
    file_types=[DB_SQL]
).add_a_renderer(
    submodule='django.DjangoRenderer',
    file_types=[DB_DJANGO]
).add_a_renderer(
    submodule='excel.ExcelRenderer',
    file_types=writers.get_all_formats()
).add_a_renderer(
    submodule='_texttable.TextTableRenderer',
    file_types=['texttable']
)
