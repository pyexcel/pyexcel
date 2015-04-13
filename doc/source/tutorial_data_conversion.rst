Sheet: Data conversion
=======================

.. testcode::
   :hide:

   >>> import pyexcel as pe
   >>> from pyexcel._compact import OrderedDict
   >>> import pyexcel.ext.xls
   >>> content = OrderedDict()
   >>> content.update({"Name": ["Adam", "Beatrice", "Ceri", "Dean"]})
   >>> content.update({"Age": [28, 29, 30, 26]})
   >>> pe.save_as(adict=content, dest_file_name="your_file.xls")


Suppose you want to process the following excel data :

========= ====
Name      Age
========= ====
Adam      28
Beatrice  29
Ceri      30
Dean      26
========= ====


Convert to records
---------------------

Here are the example code::
   
   >>> import pyexcel as pe
   >>> import pyexcel.ext.xls # import it to handle xls file
   >>> records = pe.get_records(file_name="your_file.xls")
   >>> for record in records:
   ...     print("%s is aged at %d" % (record['Name'], record['Age']))
   Adam is aged at 28
   Beatrice is aged at 29
   Ceri is aged at 30
   Dean is aged at 26

Convert to ordered dictionary
-----------------------------------

Here are the example code::
   
   >>> import pyexcel as pe
   >>> import pyexcel.ext.xls # import it to handle xls file
   >>> adict = pe.get_dict(file_name="your_file.xls")
   >>> for key in adict.keys():
   ...     print("Column '%s' contains:" % key)
   ...     for value in adict[key]:
   ...          print(value)
   Column 'Name' contains:
   Adam
   Beatrice
   Ceri
   Dean
   Column 'Age' contains:
   28.0
   29.0
   30.0
   26.0
