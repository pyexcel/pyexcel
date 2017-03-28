"""
    pyexcel.sources.factory
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Data source registration

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import logging

from pyexcel._compact import with_metaclass
from pyexcel.internal.source_meta import MetaForSourceRegistryOnly
import pyexcel.constants as constants


log = logging.getLogger(__name__)


class Source(with_metaclass(MetaForSourceRegistryOnly, object)):
    """ A command source for get_sheet, get_book, save_as and save_book_as

    This can be used to extend the function parameters once the custom
    class inherit this and register it with corresponding source registry
    """
    fields = [constants.SOURCE]
    attributes = []
    targets = []
    actions = []
    key = constants.SOURCE

    def __init__(self, source=None, **keywords):
        self.__source = source
        self.__keywords = keywords

    def get_source_info(self):
        return (None, None)

    @classmethod
    def is_my_business(cls, action, **keywords):
        """
        If all required keys are present, this source is activated
        """
        statuses = [_has_field(field, keywords) for field in cls.fields]
        results = [status for status in statuses if status is False]
        return len(results) == 0

    def write_data(self, content):
        raise NotImplementedError("")

    def get_data(self):
        raise NotImplementedError("")

    def get_internal_stream(self):
        raise NotImplementedError("")


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None
