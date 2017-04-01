"""
    pyexcel.plugin.renderers.db_renderer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into django models

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.renderer import Renderer


class DbRenderer(Renderer):

    def get_io(self):
        raise Exception("No io for this renderer")

    def render_sheet_to_file(self, file_name, sheet, **keywords):
        raise NotImplementedError("We are not writing to file")

    def render_book_to_file(self, file_name, book, **keywords):
        raise NotImplementedError("We are not writing to file")
