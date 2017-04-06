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


class MetaForRendererRegistryOnly(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(MetaForRendererRegistryOnly, cls).__init__(
            name, bases, nmspc)
        renderer.register_a_plugin(cls)


class MetaForParserRegistryOnly(type):
    def __init__(cls, name, bases, nmspc):
        super(MetaForParserRegistryOnly, cls).__init__(
            name, bases, nmspc)
        parser.register_a_plugin(cls)


class MetaForSourceRegistryOnly(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(MetaForSourceRegistryOnly, cls).__init__(
            name, bases, nmspc)
        source.register_a_plugin(cls)
