import pyexcel

# "example.csv","example.ods","example.xls", "example.xlsm"
spreadsheet = pyexcel.Reader("example.xlsx") 

for value in spreadsheet.columns():
    print value