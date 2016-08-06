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

_attributes = {
    "input-read": [],
    "sheet-read": [],
    "sheet-write": [],
    "book-read": [],
    "book-write": []
}


class LazySource:
    loaded = False

    @classmethod
    def get_sources(cls):
        if cls.loaded is False:
            register_sources(sources)
            cls.loaded = True


def get_book_rw_attributes():
    LazySource.get_sources()
    return set(_attributes["book-read"]).intersection(
        set(_attributes["book-write"]))


def get_book_w_attributes():
    LazySource.get_sources()
    return set(_attributes["book-write"]).difference(
        set(_attributes["book-read"]))


def get_sheet_rw_attributes():
    LazySource.get_sources()
    return set(_attributes["sheet-read"]).intersection(
        set(_attributes["sheet-write"]))


def get_sheet_w_attributes():
    LazySource.get_sources()
    return set(_attributes["sheet-write"]).difference(
        set(_attributes["sheet-read"]))


def register_sources(sources):
    for source in sources:
        for target in source.targets:
            for action in source.actions:
                register_a_source(target, action, source)


def register_a_source(target, action, source):
    key = "%s-%s" % (target, action)
    _sources[key].append(source)
    for target in source.targets:
        for attr in source.attributes:
            _attributes[key].append(attr)


def _get_generic_source(target, action, **keywords):
    LazySource.get_sources()
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
