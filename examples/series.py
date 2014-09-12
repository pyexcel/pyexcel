from pyexcel import SeriesReader
from pyexcel.utils import to_dict, to_array
from pyexcel.filters import OddRowFilter, EvenColumnFilter
import json


reader = SeriesReader("example_series.ods")
data = to_dict(reader)
print json.dumps(data)

data = to_array(reader.rows())
print data

data = to_array(reader.columns())
print data

reader.filter(OddRowFilter())
data = to_array(reader)
print data

reader.filter(EvenColumnFilter())
data = to_dict(reader)
print data