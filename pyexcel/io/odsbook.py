# Copyright 2011 Marco Conti

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Thanks to grt for the fixes
import datetime
import ezodf2 as ezodf
from pyexcel.sheets import (STRING_FORMAT,
                            FLOAT_FORMAT, EMPTY,
                            DATE_FORMAT, BOOLEAN_FORMAT)


def float_value(value):
    ret = float(value)
    return ret


def date_value(value):
    tokens = value.split('-')
    year = int(tokens[0])
    month = int(tokens[1])
    day = int(tokens[2])
    ret = datetime.date(year, month, day)
    return ret


def time_value(value):
    hour = int(value[2:4])
    minute = int(value[5:7])
    second = int(value[8:10])
    ret = datetime.time(hour, minute, second)
    return ret


def boolean_value(value):
    return value


ODS_FORMAT_CONVERSION = {
    "float": FLOAT_FORMAT,
    "date": DATE_FORMAT,
    "time": DATE_FORMAT,
    "boolean": BOOLEAN_FORMAT,
    "percentage": FLOAT_FORMAT,
    "currency": FLOAT_FORMAT
}


VALUE_CONVERTERS = {
    "float": float_value,
    "date": date_value,
    "time": time_value,
    "boolean": boolean_value,
    "percentage": float_value,
    "currency": float_value
}


VALUE_TOKEN = {
    "float": "value",
    "date": "date-value",
    "time": "time-value",
    "boolean": "boolean-value",
    "percentage": "value",
    "currency": "value"
}


class ODSBook:

    def __init__(self, file):
        """Load the file"""
        self.doc = ezodf.opendoc(file)
        self.SHEETS = {}
        self.sheet_names = []
        for sheet in self.doc.sheets:
            self.readSheet(sheet)

    def readSheet(self, sheet):
        """reads a sheet in the sheet dictionary, storing each sheet
        as an array (rows) of arrays (columns)"""
        table = []
        for row in range(sheet.nrows()):
            rows = []
            for column, cell in enumerate(sheet.row(row)):
                ret = self._read_cell(cell)
                rows.append(ret)
            # if row contained something
            table.append(rows)

        self.SHEETS[sheet.name] = table
        self.sheet_names.append(sheet.name)

    def _read_cell(self, cell):
        cell_type = cell.value_type
        ret = None
        if cell_type in ODS_FORMAT_CONVERSION:
            value = cell.value
            n_value = VALUE_CONVERTERS[cell_type](value)
            ret = n_value
        else:
            if cell.value is None:
                ret = ""
            else:
                ret = cell.value
        return ret

    def sheets(self):
        return self.SHEETS


class ODSSheetWriter:
    """
    ODS sheet writer
    """

    def __init__(self, book, name):
        self.doc = book
        if name:
            sheet_name = name
        else:
            sheet_name = "pyexcel_sheet1"
        self.sheet = ezodf.Sheet(sheet_name)
        self.current_row = 0

    def set_size(self, size):
        print(size)
        self.sheet.reset(size=size)

    def write_row(self, array):
        """
        write a row into the file
        """
        count = 0
        for cell in array:
            self.sheet[self.current_row, count].set_value(cell)
            count += 1
        self.current_row += 1

    def close(self):
        """
        This call writes file

        """
        self.doc.sheets += self.sheet


class ODSWriter:
    """
    open document spreadsheet writer

    """
    def __init__(self, file):
        self.doc = ezodf.newdoc(doctype="ods", filename=file)

    def create_sheet(self, name):
        """
        write a row into the file
        """
        return ODSSheetWriter(self.doc, name)

    def close(self):
        """
        This call writes file

        """
        self.doc.save()
