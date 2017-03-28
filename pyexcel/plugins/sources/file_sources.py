import pyexcel.internal.renderer_meta as renderers
import pyexcel.parsers as parsers
from pyexcel.sources import Source
from pyexcel.exceptions import FileTypeNotSupported
from pyexcel._compact import is_string
import pyexcel.constants as constants
from . import params


class FileSource(Source):
    """
    Write into presentational file
    """
    @classmethod
    def is_my_business(cls, action, **keywords):
        status = super(FileSource, cls).is_my_business(
            action, **keywords)
        if status:
            file_name = keywords.get(params.FILE_NAME, None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = _find_file_type_from_file_name(file_name,
                                                               action)
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get(params.FILE_TYPE)

            if cls.can_i_handle(action, file_type):
                status = True
            else:
                status = False
        return status

    @classmethod
    def can_i_handle(cls, action, file_type):
        return False


class InputSource(FileSource):
    """
    Get excel data from file source
    """
    @classmethod
    def can_i_handle(cls, action, file_type):
        __file_type = None
        if file_type:
            __file_type = file_type.lower()
        if action == constants.READ_ACTION:
            status = __file_type in parsers.get_all_file_types()
        else:
            status = False
        return status


class OutputSource(FileSource):
    """
    Get excel data from file source
    """
    key = params.FILE_TYPE

    @classmethod
    def can_i_handle(cls, action, file_type):
        if action == constants.WRITE_ACTION:
            status = file_type.lower() in tuple(
                renderers.get_all_file_types())
        else:
            status = False
        return status


def _find_file_type_from_file_name(file_name, action):
    if action == 'read':
        list_of_file_types = parsers.get_all_file_types()
    else:
        list_of_file_types = renderers.get_all_file_types()
    file_types = []
    lowercase_file_name = file_name.lower()
    for a_supported_type in list_of_file_types:
        if lowercase_file_name.endswith(a_supported_type):
            file_types.append(a_supported_type)
    if len(file_types) > 1:
        file_types = sorted(file_types, key=lambda x: len(x))
        file_type = file_types[-1]
    elif len(file_types) == 1:
        file_type = file_types[0]
    else:
        file_type = lowercase_file_name.split('.')[-1]
        raise FileTypeNotSupported(
            constants.FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))

    return file_type
