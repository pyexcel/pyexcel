# pyexcel [![Build Status](https://api.travis-ci.org/chfw/pyexcel.png)](http://travis-ci.org/chfw/pyexcel) [![codecov.io](https://codecov.io/github/chfw/pyexcel/coverage.png)](https://codecov.io/github/chfw/pyexcel)

Python Wrapper for reading uniform distributed data table in csv, ods, xls, and xlsx files


## Example

Suppose you have a csv, xls, xlsx file as the following:

```
1,2,3 <- row starts at 0 -\
4,5,6                      > row_range()
7,8,9 <- number_of_rows()-/
^   ^
|   number_of_columns() -\
|                         > column_range()
column starts at 0      -/
```

The following code:

```python
import pyexcel

spreadsheet = pyexcel.Reader("example.csv") # "example.xls","example.xlsx","example.ods"

for r in spreadsheet.row_range():
    for c in spreadsheet.column_range():
        print spreadsheet.cell_value(r, c)
```

will print them out as:

```
1
2
3
4
5
6
7
8
9
```

And the following code:

```python
import pyexcel

spreadsheet = pyexcel.Reader("example.csv") # "example.xls","example.xlsx","example.ods"

print spreadsheet.json()
```

will print them out as json:

```
[["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
```

## Dependencies

* odfpy
* xlrd
* openpyxl


## Note

ods reader is made by [Marco Conti](https://github.com/marcoconti83/read-ods-with-odfpy)