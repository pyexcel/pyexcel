import pyexcel

# "example.csv","example.xlsx","example.ods", "example.xlsm"
spreadsheet = pyexcel.Reader("example.xls") 

for value in spreadsheet:
    print value