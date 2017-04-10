from lml.plugin import scan_plugins
from pyexcel.internal.plugins import PyexcelPluginManager
from pyexcel.internal.source_plugin import SourcePluginManager
from pyexcel.internal.generators import SheetStream, BookStream  # noqa


renderer = PyexcelPluginManager('renderer')
parser = PyexcelPluginManager('parser')
source = SourcePluginManager()

BLACK_LIST = ['pyexcel_io', 'pyexcel_webio',
              'pyexcel_xlsx', 'pyexcel_xls',
              'pyexcel_ods3', 'pyexcel_ods',
              'pyexcel_odsr', 'pyexcel_xlsxw']
WHITE_LIST = [
    'pyexcel.plugins.parsers',
    'pyexcel.plugins.renderers',
    'pyexcel.plugins.sources',
]

MARKER = '__pyexcel_plugins__'

scan_plugins('pyexcel_', MARKER, 'pyexcel', BLACK_LIST, WHITE_LIST)
