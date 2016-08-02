from . import file_source_output, database
from . import file_source_input, http, pydata
from .factory import SourceFactory


sources = (http.sources + file_source_input.sources + pydata.sources +
           file_source_output.sources + database.sources)

SourceFactory.register_sources(sources)
