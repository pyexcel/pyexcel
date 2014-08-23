pyexcel
=======

Python Wrapper for reading csv, xls, and xlsx files


Example
=======

Suppose you have a csv, xls, xlsx file as the following:

| |A|B|C|
|-|-|-|-|
|1|1|2|3|
|2|2|3|4|
|3|3|4|5|


The following code will print out the first column:

```python
import pyexcel

spreadsheet = pyexcel.Reader("your.csv") # "your.xls", "your.xlsx"

for i in spreadsheet.range():
    print spreadsheet.cell_value(i, 1)
```
