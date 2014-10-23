import pyexcel

# "example.csv","example.xlsx","example.xls", "example.xlsm"
spreadsheet = pyexcel.Reader("example.ods") 

for value in spreadsheet.rows():
    print value