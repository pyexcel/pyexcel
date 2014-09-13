from pyexcel import SeriesReader, FilterableReader
from pyexcel.utils import to_dict, to_array
from pyexcel.filters import OddRowFilter, EvenColumnFilter
import json
from pyexcel import Writer


reader = SeriesReader("example_series.ods")
data = to_dict(reader)
print json.dumps(data)

data = to_array(reader.rows())
print data

data = to_array(reader.columns())
print data

reader.filter(OddRowFilter())
print reader.hat()

reader.filter(EvenColumnFilter())
print reader.hat()
data = to_dict(reader)
print data

w = Writer("example_series_filter.xls")
w.write_reader(reader)
w.close()