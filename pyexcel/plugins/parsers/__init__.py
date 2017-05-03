"""
    pyexcel.plugins.parsers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A list of built-in parsers

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.plugins import READERS
from pyexcel_io.constants import DB_SQL, DB_DJANGO

from pyexcel.internal.common import PyexcelPluginList


PyexcelPluginList(__name__).add_a_parser(
    submodule='excel.ExcelParser',
    file_types=READERS.get_all_formats()
).add_a_parser(
    submodule='sqlalchemy.SQLAlchemyExporter',
    file_types=[DB_SQL]
).add_a_parser(
    submodule='django.DjangoExporter',
    file_types=[DB_DJANGO]
)
