from pyexcel.presentation import STRINGIFICATION

def present_matrix(matrix_instance):
    return str(matrix_instance.__class__)

STRINGIFICATION["pyexcel.sheets.matrix.Matrix"] = present_matrix

