import pyexcel as pe

sheet = pe.load("tutorial_datatype_01.xls", name_colmns_by_row=0)
print sheet.to_dict()
#{u'userid': [10120.0, 10121.0, 10122.0], u'name': [u'Adam', u'Bella', u'Cedar']}
sheet.column.format(0, str)
print sheet.to_dict()
#{u'userid': ['10120.0', '10121.0', '10122.0'], u'name': [u'Adam', u'Bella', u'Cedar']}