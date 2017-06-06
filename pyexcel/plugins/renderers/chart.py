"""
    pyexcel_chart
    ~~~~~~~~~~~~~~~~~~~

    chart drawing plugin for pyexcel

    :copyright: (c) 2016-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for further details
"""
from lml.plugin import PluginManager

from pyexcel.renderer import BinaryRenderer
import pyexcel._compact as compact


DEFAULT_TITLE = 'pyexce-chart renders'
DEFAULT_CHART_TYPE = 'bar'


class ChartManager(PluginManager):
    def __init__(self):
        PluginManager.__init__(self, 'chart')

    def get_a_plugin(self, key, **keywords):
        self._logger.debug("get a plugin called")
        plugin = self.load_me_now(key)
        return plugin(key)

    def raise_exception(self, key):
        raise Exception("No support for " + key)


MANAGER = ChartManager()


class ChartRenderer(BinaryRenderer):

    def __init__(self, file_type):
        BinaryRenderer.__init__(self, file_type)
        if not compact.PY2:
            self.WRITE_FLAG = 'wb'

    def render_sheet(self, sheet, title=DEFAULT_TITLE,
                     chart_type=DEFAULT_CHART_TYPE,
                     **keywords):
        charter = MANAGER.get_a_plugin(chart_type)
        chart_content = charter.render_sheet(
            sheet, title=title, **keywords)
        self._write_content(chart_content)

    def render_book(self, book, title=DEFAULT_TITLE,
                    chart_type=DEFAULT_CHART_TYPE, **keywords):
        charter = MANAGER.get_a_plugin(chart_type)
        chart_content = charter.render_book(
            book, title=title, **keywords)
        self._write_content(chart_content)

    def _write_content(self, chart_content):
        if compact.PY2:
            chart_content.decode('utf-8')
        self._stream.write(chart_content)
