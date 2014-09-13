# pyexcel [![Build Status](https://api.travis-ci.org/chfw/pyexcel.png)](http://travis-ci.org/chfw/pyexcel) [![codecov.io](https://codecov.io/github/chfw/pyexcel/coverage.png)](https://codecov.io/github/chfw/pyexcel)

Python Wrapper for reading and writing uniform distributed data table in csv, ods, xls, xlsx and xlsm files


## Example

### Reading an excel file
Suppose you have a csv, xls, xlsx file as the following:

```
1,2,3
4,5,6
7,8,9
```

The following code will give you the data in json

```python
from pyexcel import Reader
from pyexcel.utils import to_array
import json

# "example.xls","example.xlsx","example.ods", "example.xlsm"
reader = Reader("example.csv")
data = to_array(reader.rows())
print json.dumps(data)
```

The output is:

```
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

Suppose you have a csv, xls, xlsx file as the following:

```
Column 1, Column 2, Column 3
1,4,7
2,5,8
3,6,9
```

The following code will give you data series in a dictionary.

```python
from pyexcel import SeriesReader
from pyexcel.utils import to_dict

# "example.xls","example.xlsx","example.ods", "example.xlsm"
reader = SeriesReader("example.csv")
data = to_dict(reader)
print data
```

The output is:

```
{"Column 2": [4, 5, 6], "Column 3": [7, 8, 9], "Column 1": [1, 2, 3]}
```

### Writing an excel file

Suppose you have an array as the following:

```
1,2,3
4,5,6
7,8,9
```

The following code will write it as an excel file of your choice.

```python
from pyexcel import Writer

array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# "output.xls" "output.xlsx" "output.ods" "output.xlsm"
writer = Writer("output.csv")
writer.write_array(array)
writer.close()
```

Suppose you have a dictionary as the following:

```
Column 1, Column 2, Column 3
1,4,7
2,5,8
3,6,9
```

The following code will write it as an excel file of your choice.

```python
from pyexcel import Writer

example_dict = {"Column 1": [1, 2, 3], "Column 2": [4, 5, 6], "Column 3": [7, 8, 9]}
# "output.xls" "output.xlsx" "output.ods" "output.xlsm"
writer = Writer("output.csv")
writer.write_dict(example_dict)
writer.close()
```


## Dependencies

* odfpy
* xlrd
* xlwt

## Credits

ODSReader is written by [Marco Conti](https://github.com/marcoconti83/read-ods-with-odfpy)