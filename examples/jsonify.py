import pyexcel

spreadsheet = pyexcel.Reader("example.csv")  # "example.xls","example.xlsx","example.ods"

print spreadsheet.json()