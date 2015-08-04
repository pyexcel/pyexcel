from pyexcel import SeriesReader
from pyexcel.utils import to_dict
from pyexcel.formatters import ColumnFormatter


reader = SeriesReader("tutorial_datatype_01.xls")
print(to_dict(reader))
#{u'userid': [10120.0, 10121.0, 10122.0], u'name': [u'Adam', u'Bella', u'Cedar']}
formatter = ColumnFormatter(0, str)
reader.add_formatter(formatter)
to_dict(reader)
#{u'userid': ['10120.0', '10121.0', '10122.0'], u'name': [u'Adam', u'Bella', u'Cedar']}