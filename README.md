# pyexcel [![Build Status](https://api.travis-ci.org/chfw/pyexcel.png)](http://travis-ci.org/chfw/pyexcel) [![codecov.io](https://codecov.io/github/chfw/pyexcel/coverage.png)](https://codecov.io/github/chfw/pyexcel) [![Documentation Status](https://readthedocs.org/projects/pyexcel/badge/?version=latest)](https://readthedocs.org/projects/pyexcel/?badge=latest)

**pyexcel** is a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. Its mission is to let you focus on data itself and it deals with different file formats. But this library does not support fonts, colors and charts.

It was created due to the lack of uniform programming interface to access data in different formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

All great work have done by odf, xlrd and other individual developers. This library unites only the data access code.

## Installation

You can install it via pip

```
$ pip install pyexcel
```

or clone it and install it

```
$ git clone http://github.com/chfw/pyexcel.git
$ cd pyexcel
$ python setup.py install
```


## Example

### Reading a single sheet excel file
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
data = to_array(reader)
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

### Writing a single sheet excel file

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

### Read multiple sheet excel file

Suppose you have a book like this:

```
1,2,3
4,5,6
7,8,9
```
Sheet 1

```
X,Y,Z
1,2,3
4,5,6
```

Sheet 2

```
O,P,Q
3,2,1
4,3,2
```

Sheet 3

You can get a dictionary out of it by the following code:

```python
import pyexcel


reader = pyexcel.BookReader("example.xls")
my_dict = pyexcel.utils.to_dict(reader)
print my_dict
```

the output is:

```
{
u'Sheet 2': [[u'X', u'Y', u'Z'], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], 
u'Sheet 3': [[u'O', u'P', u'Q'], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]], 
u'Sheet 1': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
}
```

### Write multiple sheet excel file

Suppose you have previous data as a dictionary and you want to save it as multiple sheet excel file:

```python
import pyexcel


content = {
    'Sheet 2': 
        [
            ['X', 'Y', 'Z'], 
            [1.0, 2.0, 3.0], 
            [4.0, 5.0, 6.0]
        ], 
    'Sheet 3': 
        [
            ['O', 'P', 'Q'], 
            [3.0, 2.0, 1.0], 
            [4.0, 3.0, 2.0]
        ], 
    'Sheet 1': 
        [
            [1.0, 2.0, 3.0], 
            [4.0, 5.0, 6.0], 
            [7.0, 8.0, 9.0]
        ]
}
writer = pyexcel.BookWriter("myfile.ods")
writer.write_book_from_dict(content)
writer.close()
```

You shall get a ods file 

### Access individual cell values in the excel file

For single sheet file, you can regard it as two dimensional array if you use `Reader` class. So, you access each cell via this syntax: reader[row][column]

For multiple sheet file, you can regard it as three dimensional array if you use `BookReader`. So, you access each cell via this syntax: reader[sheet_index][row][column] or reader["sheet_name"][row][column]

## Documentation

It is hosted in [pyhosted](https://pythonhosted.org/pyexcel/)

## Dependencies

* odfpy
* xlrd
* xlwt

## Credits

ODSReader is written by [Marco Conti](https://github.com/marcoconti83/read-ods-with-odfpy)