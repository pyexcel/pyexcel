import json
from .base import Source, one_sheet_tuple, _has_field
from .._compact import PY2, is_string, is_generator
from ..constants import KEYWORD_FILE_NAME, KEYWORD_FILE_TYPE, DEFAULT_SHEET_NAME


class JsonSource(Source):
    """
    Write into json file
    """
    @classmethod
    def is_my_business(cls, action, **keywords):
        statuses = [_has_field(field, keywords) for field in cls.fields]
        results = filter(lambda status: status is False, statuses)
        if not PY2:
            results = list(results)
        status = len(results) == 0
        if status:
            file_name = keywords.get(KEYWORD_FILE_NAME, None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = file_name.split(".")[-1]
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get(KEYWORD_FILE_TYPE)

            if action == 'write' and file_type == "json":
                status = True
            else:
                status = False
        return status


class JsonSheetSource(JsonSource):
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

    def write_data(self, book):
        if self.keywords.get('single_sheet_in_book', False):
            keys = list(book.keys())
            JsonSheetSource.write_data(book[keys[0]])
        else:
            with open(self.file_name, 'w') as jsonfile:
                jsonfile.write(json.dumps(book.to_dict(), sort_keys=True))
