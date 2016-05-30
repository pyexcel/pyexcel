from pyexcel.sources.rendererfactory import Renderer
from nose.tools import raises


@raises(NotImplementedError)
def test_render_sheet():
    r = Renderer("xls")
    r.render_sheet("something")