from pyexcel.presentation import STRINGIFICATION

def present_matrix(matrix_instance):
    return "pyexcel.sheets.matrix.Matrix"

def class_name(name):
    return "<class '%s'>" % name

STRINGIFICATION[class_name("pyexcel.sheets.matrix.Matrix")] = present_matrix

