from texttable import Texttable
from pyexcel.formatters import to_format
from pyexcel.sources.rendererfactory import Renderer
from pyexcel._compact import is_generator


class TextTableRenderer(Renderer):

    file_types = ('texttable',)

    def render_sheet(self, sheet):
        self.stream.write(render_text_table(sheet,
                                            self.file_type,
                                            self.write_title))


def render_text_table(sheet, _, write_title):
    content = ""
    if write_title:
        content += "%s:\n" % sheet.name
    table = Texttable(max_width=0)
    data = sheet.to_array()
    if is_generator(data):
        data = list(data)
    table.set_cols_dtype(['t'] * len(data[0]))
    if len(sheet.colnames) > 0:
        table.set_chars(['-', '|', '+', '='])
        table.header(list(_cleanse_a_row(data[0])))
    else:
        table.add_row(list(_cleanse_a_row(data[0])))
    for sub_array in data[1:]:
        new_array = _cleanse_a_row(sub_array)
        table.add_row(list(new_array))
    content += table.draw()
    return content


def _cleanse_a_row(row):
    for item in row:
        if item == "":
            yield(" ")
        else:
            yield(to_format(str, item))


renderers = (TextTableRenderer,)
