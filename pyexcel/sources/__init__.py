from . import file_source_output, database
from . import file_source_input, http, pydata


sources = (http.sources + file_source_input.sources + pydata.sources +
           file_source_output.sources + database.sources)



_sources = {
    "input-read": [],
    "sheet-write": [],
    "book-write": [],
    "book-read": [],
    "sheet-read": []
}


def register_sources(sources):
    for source in sources:
        for target in source.targets:
            for action in source.actions:
                register_a_source(target, action, source)


def register_a_source(target, action, source):
    key = "%s-%s" % (target, action)
    _sources[key].append(source)


def _get_generic_source(target, action, **keywords):
    key = "%s-%s" % (target, action)
    for source in _sources[key]:
        if source.is_my_business(action, **keywords):
            s = source(**keywords)
            return s
    return None


def get_source(**keywords):
    source = _get_generic_source(
        'input',
        'read',
        **keywords)
    if source is None:
        source = _get_generic_source(
            'sheet',
            'read',
            **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_book_source(**keywords):
    source = _get_generic_source(
        'input',
        'read',
        **keywords)
    if source is None:
        source = _get_generic_source(
            'book',
            'read',
            **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_writable_source(**keywords):
    source = _get_generic_source(
        'sheet',
        'write',
        **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_writable_book_source(**keywords):
    source = _get_generic_source(
        'book',
        'write',
        **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


register_sources(sources)