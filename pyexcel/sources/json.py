import json

from .._compact import is_string
from ..constants import KEYWORD_FILE_NAME, KEYWORD_FILE_TYPE

from .base import Source
from .factory import SourceFactory


class TextSource(Source):
    """
    Write into json file
    """
    @classmethod
    def is_my_business(cls, action, **keywords):
        status = super(JsonSource, cls).is_my_business(action, **keywords)
        if status:
            file_name = keywords.get(KEYWORD_FILE_NAME, None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = file_name.split(".")[-1]
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get(KEYWORD_FILE_TYPE)

            if cls.can_i_handle(action, file_type):
                status = True
            else:
                status = False
        return status

    @classmethod
    def can_i_handle(cls, action, file_type):
        return False

        
class JsonSource(Source):
    """
    Write into json file
    """
    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == 'write' and file_type == "json":
            status = True
        return status


class JsonSheetSource(JsonSource):
    """
    Write a two dimensional array into json format
    """
    fields = [KEYWORD_FILE_NAME]

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords
    
    def write_data(self, sheet):
        data = self.transform_data(sheet)
        with open(self.file_name, 'w') as jsonfile:
            jsonfile.write(json.dumps(data, sort_keys=True))

    def transform_data(self, sheet):
        table = sheet.to_array()
        if hasattr(sheet, 'colnames'):
            colnames = sheet.colnames
            rownames = sheet.rownames
            # In the following, row[0] is the name of each row
            if colnames and rownames:
                table = dict((row[0], dict(zip(colnames, row[1:])))
                             for row in table[1:])
            elif colnames:
                table = [dict(zip(colnames, row)) for row in table[1:]]
            elif rownames:
                table = dict((row[0], row[1:]) for row in table)
        else:
            table = list(table)
        return table


class JsonBookSource(JsonSheetSource):
    """
    Write a dictionary of two dimensional arrays into json format
    """
    def write_data(self, book):
        if self.keywords.get('single_sheet_in_book', False):
            keys = list(book.keys())
            JsonSheetSource.write_data(book[keys[0]])
        else:
            with open(self.file_name, 'w') as jsonfile:
                jsonfile.write(json.dumps(book.to_dict(), sort_keys=True))


SourceFactory.register_a_source("sheet", "write", JsonSheetSource)
SourceFactory.register_a_source("book", "write", JsonBookSource)
