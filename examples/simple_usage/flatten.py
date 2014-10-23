import pyexcel

# "example.xls","example.xlsx","example.ods", "example.xlsm"
spreadsheet = pyexcel.Reader("example.csv") 

for r in spreadsheet.row_range():
    for c in spreadsheet.column_range():
        print spreadsheet.cell_value(r, c)