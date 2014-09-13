from pyexcel import SeriesReader, FilterableReader
from pyexcel.utils import to_dict, to_array
from pyexcel.filters import OddRowFilter, EvenColumnFilter
import json
from pyexcel import Writer


reader = SeriesReader("example_series.ods")
data = to_dict(reader)
print json.dumps(data)

print reader.series()

data = to_array(reader.enumerate())
print data
data = to_array(reader.vertical())
print data
data = to_array(reader.rvertical())
print data
data = to_array(reader.reverse())
print data

data = to_array(reader.rows())
print data

data = to_array(reader.rrows())
print data

data = to_array(reader.columns())
print data

data = to_array(reader.rcolumns())
print data

reader.filter(OddRowFilter())
print reader.series()

reader.filter(EvenColumnFilter())
print reader.series()
data = to_dict(reader)
print data

w = Writer("example_series_filter.xls")
w.write_reader(reader)
w.close()