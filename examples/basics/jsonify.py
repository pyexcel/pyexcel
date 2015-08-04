import pyexcel as pe
import json

# "example.xls","example.xlsx","example.ods", "example.xlsm"
sheet = pe.Sheet("example.csv")
print(json.dumps(sheet.to_array()))