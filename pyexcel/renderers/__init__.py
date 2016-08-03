from . import _texttable as texttable
from . import _excel as excel

renderers = texttable.renderers + excel.renderers

try:
    import pyexcel_text as text
    renderers += text.renderers
except ImportError:
    pass


renderer_factories = {}


def get_renderer(file_type):
    renderer_class = renderer_factories.get(file_type)
    return renderer_class(file_type)


def register_renderers(renderers):
    for renderer in renderers:
        for file_type in renderer.file_types:
            renderer_factories[file_type] = renderer


register_renderers(renderers)
