from pyexcel_io.utils import AVAILABLE_WRITERS, AVAILABLE_READERS
from pyexcel_io.constants import DB_SQL, DB_DJANGO
import pyexcel_io.manager as manager


def get_excel_reader_formats():
    all_formats = set(list(manager.reader_factories.keys()) +
                      list(AVAILABLE_READERS.keys()))
    all_formats = all_formats.difference(set([DB_SQL, DB_DJANGO]))
    return all_formats


def get_excel_formats():
    all_formats = set(tuple(AVAILABLE_WRITERS.keys()) +
                      tuple(manager.get_writers()))
    all_formats = all_formats.difference(set([DB_SQL, DB_DJANGO]))
    return all_formats
