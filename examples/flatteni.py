import pyexcel

# "example.xls","example.xlsx","example.ods", "example.xlsm"
spreadsheet = pyexcel.Reader("example.csv") 

for value in spreadsheet:
    print value