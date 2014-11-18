from pyexcel.presentation import STRINGIFICATION
import sys

def present_matrix(matrix_instance):
    return "pyexcel.sheets.matrix.Matrix"

def class_name(name):
    if sys.version_info[0] > 2:
        return "<class '%s'>" % name
    else:
        return name

STRINGIFICATION[class_name("pyexcel.sheets.matrix.Matrix")] = present_matrix

