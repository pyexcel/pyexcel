"""
    pyexcel.ext.odsreader
    ~~~~~~~~~~~~~~~~~~~~~~

    ODSReader

    :copyright: (c) 2011 by Marco Conti
    :license: Apache License 2.0
"""
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
import odf.opendocument
from odf.table import *
from odf.text import P
from odf.namespaces import OFFICENS
from pyexcel.common import Cell as pycell
from pyexcel.common import (STRING_FORMAT,
                            FLOAT_FORMAT, EMPTY,
                            DATE_FORMAT, BOOLEAN_FORMAT)
from csvbook import CSVSheet


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
    if value == "true":
        ret = True
    else:
        ret = False
    return ret


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
    

class ODSReader:

    def __init__(self, file):
        """Load the file"""
        self.doc = odf.opendocument.load(file)
        self.SHEETS = {}
        self.sheet_names = []
        for sheet in self.doc.spreadsheet.getElementsByType(Table):
            self.readSheet(sheet)
    
    def readSheet(self, sheet):
        """reads a sheet in the sheet dictionary, storing each sheet as an array (rows) of arrays (columns)"""
        name = sheet.getAttribute("name")
        rows = sheet.getElementsByType(TableRow)
        arrRows = []
        
        # for each row
        for row in rows:
            arrCells = []
            cells = row.getElementsByType(TableCell)
            has_value = False
            
            # for each cell
            for cell in cells:
                # repeated value?
                repeat = cell.getAttribute("numbercolumnsrepeated")
                if(not repeat):
                    has_value = True
                    cell_type = cell.getAttrNS(OFFICENS, "value-type")
                    if cell_type == "float" or cell_type == "currency" or cell_type == "percentage":
                        value_token = "value"
                    else:
                        value_token = "%s-value" % cell_type
                    if cell_type == "string":
                        ps = cell.getElementsByType(P)
                        textContent = ""
                        # for each text node
                        for p in ps:
                            for n in p.childNodes:
                                if (n.nodeType == 3):
                                    textContent = textContent + unicode(n.data)
                        arrCells.append(pycell(STRING_FORMAT, textContent))
                    else:
                        if cell_type in ODS_FORMAT_CONVERSION:
                            value = cell.getAttrNS(OFFICENS, value_token)
                            n_value = VALUE_CONVERTERS[cell_type](value)
                            n_type = ODS_FORMAT_CONVERSION[cell_type]
                            arrCells.append(pycell(n_type, n_value))
                        else:
                            ps = cell.getElementsByType(P)
                            textContent = ""
                            # for each text node
                            for p in ps:
                                for n in p.childNodes:
                                    if (n.nodeType == 3):
                                        textContent = textContent + unicode(n.data)
                            if len(textContent):
                                arrCells.append(pycell(STRING_FORMAT, textContent))
                            else:
                                arrCells.append(pycell(EMPTY, ""))
                else:
                    r = int(repeat)
                    for i in range(0, r):
                        arrCells.append(pycell(EMPTY, ""))
            # if row contained something
            if(len(arrCells) and has_value):
                arrRows.append(arrCells)
                
        self.SHEETS[name] = arrRows
        self.sheet_names.append(name)


class ODSSheet(CSVSheet):
    """
    ods sheet
    """
    def cell_value(self, row, column):
        """
        Random access to the csv cells
        """
        cell = self.sheet[row][column]
        return cell


class ODSBook:
    """
    ODS Book reader

    It reads ods file
    """

    def __init__(self, file):
        self.ods = ODSReader(file)

    def sheets(self):
        ret = {}
        for name in self.ods.SHEETS.keys():
            ret[name] = ODSSheet(self.ods.SHEETS[name])
        return ret
