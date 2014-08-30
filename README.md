pyexcel
=======

Python Wrapper for reading uniform distributed data table in csv, xls, and xlsx files


Example
=======

Suppose you have a csv, xls, xlsx file as the following:

```
1,2,3 <- row starts at 0 -\
2,3,4                      > row_range()
3,4,5 <- number_of_rows()-/
^   ^
|   number_of_columns() -\
|                         > column_range()
column starts at 0      -/
```

The following code will print out the first column:

```python
import pyexcel

spreadsheet = pyexcel.Reader("your.csv") # "your.xls", "your.xlsx"

for r in spreadsheet.row_range():
    for c in spreadsheet.column_range():
        print spreadsheet.cell_value(r, j)
```
