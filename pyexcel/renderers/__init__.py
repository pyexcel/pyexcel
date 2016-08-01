from . import _texttable as texttable
from . import _excel as excel
from .factory import RendererFactory

renderers = texttable.renderers + excel.renderers

try:
    import pyexcel_text as text
    renderers += text.renderers
except ImportError:
    pass

RendererFactory.register_renderers(renderers)
