import pyexcel

spreadsheet = pyexcel.Reader("example.csv") # "your.xls", "your.xlsx", "your.ods"

for r in spreadsheet.row_range():
    for c in spreadsheet.column_range():
        print spreadsheet.cell_value(r, c)