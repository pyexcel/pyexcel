
def extend_pyexcel(ReaderFactory, WriterFactory):
    ReaderFactory.add_factory("test", "test")
    WriterFactory.add_factory("test", "test")
