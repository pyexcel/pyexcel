class RendererFactory:
    renderer_factories = {}

    @classmethod
    def get_renderer(self, file_type):
        renderer_class = self.renderer_factories.get(file_type)
        return renderer_class(file_type)

    @classmethod
    def register_renderers(self, renderers):
        for renderer in renderers:
            for file_type in renderer.file_types:
                self.renderer_factories[file_type] = renderer


class Renderer(object):
    def __init__(self, file_type):
        self.file_type = file_type
        self.stream = None

    def set_output_stream(self, stream):
        self.stream = stream

    def set_write_title(self, flag):
        self.write_title = flag

    def render_sheet(self, sheet):
        self.stream.write(sheet.name)

    def render_book(self, book):
        number_of_sheets = book.number_of_sheets() - 1
        for index, sheet in enumerate(book):
            self.render_sheet(sheet)
            if index < number_of_sheets:
                self.stream.write('\n')
