Sheet: Data conversion
=======================

.. _get_records_from_an_excel_sheet:

How to obtain records from an excel sheet
-------------------------------------------

.. testcode::
   :hide:

   >>> import pyexcel as pe
   >>> from pyexcel._compact import OrderedDict
   >>> content = OrderedDict()
   >>> content.update({"Name": ["Adam", "Beatrice", "Ceri", "Dean"]})
   >>> content.update({"Age": [28, 29, 30, 26]})
   >>> pe.save_as(adict=content, dest_file_name="your_file.xls")


Suppose you want to process the following excel data :

.. pyexcel-table::

   ---pyexcel:example table---
   Name,Age
   Adam,28
   Beatrice,29
   Ceri,30
   Dean,26

Here are the example code::
   
   >>> import pyexcel as pe
   >>> records = pe.get_records(file_name="your_file.xls")
   >>> for record in records:
   ...     print("%s is aged at %d" % (record['Name'], record['Age']))
   Adam is aged at 28
   Beatrice is aged at 29
   Ceri is aged at 30
   Dean is aged at 26


.. _save_an_array_to_an_excel_sheet:

How to save an python array as an excel file
---------------------------------------------

Suppose you have the following array::

   >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

And here is the code to save it as an excel file ::

   >>> import pyexcel
   >>> pyexcel.save_as(array=data, dest_file_name="example.xls")

Let's verify it::

    >>> pyexcel.get_sheet(file_name="example.xls")
    pyexcel_sheet1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example.xls")

.. _save_an_array_to_a_csv_with_custom_delimiter:

How to save an python array as a csv file with special delimiter
--------------------------------------------------------------------

Suppose you have the following array::

   >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

And here is the code to save it as an excel file ::

   >>> import pyexcel
   >>> pyexcel.save_as(array=data,
   ...                 dest_file_name="example.csv",
   ...                 dest_delimiter=':')

Let's verify it::

   >>> with open("example.csv") as f:
   ...     for line in f.readlines():
   ...         print(line.rstrip())
   ...
   1:2:3
   4:5:6
   7:8:9

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example.csv")

.. _get_a_dict_from_an_excel_sheet:

How to get a dictionary from an excel sheet
--------------------------------------------

Suppose you have a csv, xls, xlsx file as the following:


.. pyexcel-table::

   ---pyexcel:data with columns---
   Column 1,Column 2,Column 3
   1,4,7
   2,5,8
   3,6,9

.. testcode::
   :hide:

   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 2, 3],
   ...      [4, 5, 6],
   ...      [7, 8, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example_series.xls")


The following code will give you data series in a dictionary:

.. testcode::
    
   >>> import pyexcel
   >>> from pyexcel._compact import OrderedDict
   >>> my_dict = pyexcel.get_dict(file_name="example_series.xls", name_columns_by_row=0)
   >>> isinstance(my_dict, OrderedDict)
   True
   >>> for key, values in my_dict.items():
   ...     print({str(key): values})
   {'Column 1': [1, 4, 7]}
   {'Column 2': [2, 5, 8]}
   {'Column 3': [3, 6, 9]}

Please note that my_dict is an OrderedDict.

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example_series.xls")


.. _get_an_book_dict_from_an_excel_book:

How to obtain a dictionary from a multiple sheet book
-------------------------------------------------------

.. testcode::
   :hide:

   >>> a_dictionary_of_two_dimensional_arrays = {
   ...      'Sheet 1':
   ...          [
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0],
   ...              [7.0, 8.0, 9.0]
   ...          ],
   ...      'Sheet 2':
   ...          [
   ...              ['X', 'Y', 'Z'],
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0]
   ...          ],
   ...      'Sheet 3':
   ...          [
   ...              ['O', 'P', 'Q'],
   ...              [3.0, 2.0, 1.0],
   ...              [4.0, 3.0, 2.0]
   ...          ]
   ...  }
   >>> data = OrderedDict()
   >>> data.update({"Sheet 1": a_dictionary_of_two_dimensional_arrays['Sheet 1']})
   >>> data.update({"Sheet 2": a_dictionary_of_two_dimensional_arrays['Sheet 2']})
   >>> data.update({"Sheet 3": a_dictionary_of_two_dimensional_arrays['Sheet 3']})
   >>> pyexcel.save_book_as(bookdict=data, dest_file_name="book.xls")

Suppose you have a multiple sheet book as the following:

.. pyexcel-table::

   ---pyexcel:Sheet 1---
   1,2,3
   4,5,6
   7,8,9
   ---pyexcel---
   ---pyexcel:Sheet 2---
   X,Y,Z
   1,2,3
   4,5,6
   ---pyexcel---
   ---pyexcel:Sheet 3---
   O,P,Q
   3,2,1
   4,3,2

Here is the code to obtain those sheets as a single dictionary::

   >>> import pyexcel
   >>> import json
   >>> book_dict = pyexcel.get_book_dict(file_name="book.xls")
   >>> isinstance(book_dict, OrderedDict)
   True
   >>> for key, item in book_dict.items():
   ...     print(json.dumps({key: item}))
   {"Sheet 1": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}
   {"Sheet 2": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]}
   {"Sheet 3": [["O", "P", "Q"], [3, 2, 1], [4, 3, 2]]}

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("book.xls")


.. _save_an_book_dict_to_an_excel_book:
   
How to save a dictionary of two dimensional array as an excel file
--------------------------------------------------------------------

Suppose you want to save the below dictionary to an excel file ::
  
   >>> a_dictionary_of_two_dimensional_arrays = {
   ...      'Sheet 1':
   ...          [
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0],
   ...              [7.0, 8.0, 9.0]
   ...          ],
   ...      'Sheet 2':
   ...          [
   ...              ['X', 'Y', 'Z'],
   ...              [1.0, 2.0, 3.0],
   ...              [4.0, 5.0, 6.0]
   ...          ],
   ...      'Sheet 3':
   ...          [
   ...              ['O', 'P', 'Q'],
   ...              [3.0, 2.0, 1.0],
   ...              [4.0, 3.0, 2.0]
   ...          ]
   ...  }

Here is the code::

   >>> pyexcel.save_book_as(
   ...    bookdict=a_dictionary_of_two_dimensional_arrays,
   ...    dest_file_name="book.xls"
   ... )

If you want to preserve the order of sheets in your dictionary, you have to
pass on an ordered dictionary to the function itself. For example::

   >>> data = OrderedDict()
   >>> data.update({"Sheet 2": a_dictionary_of_two_dimensional_arrays['Sheet 2']})
   >>> data.update({"Sheet 1": a_dictionary_of_two_dimensional_arrays['Sheet 1']})
   >>> data.update({"Sheet 3": a_dictionary_of_two_dimensional_arrays['Sheet 3']})
   >>> pyexcel.save_book_as(bookdict=data, dest_file_name="book.xls")

Let's verify its order::

   >>> book_dict = pyexcel.get_book_dict(file_name="book.xls")
   >>> for key, item in book_dict.items():
   ...     print(json.dumps({key: item}))
   {"Sheet 2": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]}
   {"Sheet 1": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}
   {"Sheet 3": [["O", "P", "Q"], [3, 2, 1], [4, 3, 2]]}

Please notice that "Sheet 2" is the first item in the *book_dict*, meaning the order of sheets are preserved.

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("book.xls")


.. _import_excel_sheet_into_a_database_table:

How to import an excel sheet to a database using SQLAlchemy
------------------------------------------------------------

.. NOTE::

   You can find the complete code of this example in examples folder on github

Before going ahead, let's import the needed components and initialize sql
engine and table base::

   >>> from sqlalchemy import create_engine
   >>> from sqlalchemy.ext.declarative import declarative_base
   >>> from sqlalchemy import Column , Integer, String, Float, Date
   >>> from sqlalchemy.orm import sessionmaker
   >>> engine = create_engine("sqlite:///birth.db")
   >>> Base = declarative_base()
   >>> Session = sessionmaker(bind=engine)

Let's suppose we have the following database model:

   >>> class BirthRegister(Base):
   ...     __tablename__='birth'
   ...     id=Column(Integer, primary_key=True)
   ...     name=Column(String)
   ...     weight=Column(Float)
   ...     birth=Column(Date)

Let's create the table::
  
   >>> Base.metadata.create_all(engine)

Now here is a sample excel file to be saved to the table:


.. pyexcel-table::
   
   ---pyexcel:data table---
   name,weight,birth     
   Adam,3.4,2015-02-03
   Smith,4.2,2014-11-12

.. testcode::
   :hide:

   >>> import datetime
   >>> data = [
   ...    ["name", "weight", "birth"],
   ...    ["Adam", 3.4, datetime.date(2015, 2, 3)],
   ...    ["Smith", 4.2, datetime.date(2014, 11, 12)]
   ... ]
   >>> pyexcel.save_as(array=data, dest_file_name="birth.xls")

Here is the code to import it:

   >>> session = Session() # obtain a sql session
   >>> pyexcel.save_as(file_name="birth.xls", name_columns_by_row=0, dest_session=session, dest_table=BirthRegister)

Done it. It is that simple. Let's verify what has been imported to make sure.

   >>> sheet = pyexcel.get_sheet(session=session, table=BirthRegister)
   >>> sheet
   birth:
   +------------+----+-------+--------+
   | birth      | id | name  | weight |
   +------------+----+-------+--------+
   | 2015-02-03 | 1  | Adam  | 3.4    |
   +------------+----+-------+--------+
   | 2014-11-12 | 2  | Smith | 4.2    |
   +------------+----+-------+--------+

.. testcode::
   :hide:

   >>> session.close()
   >>> os.unlink('birth.db')


.. _save_a_xls_as_a_csv:

How to open an xls file and save it as csv
-------------------------------------------

.. testcode::
   :hide:

   >>> import datetime
   >>> data = [
   ...    ["name", "weight", "birth"],
   ...    ["Adam", 3.4, datetime.date(2015, 2, 3)],
   ...    ["Smith", 4.2, datetime.date(2014, 11, 12)]
   ... ]
   >>> pyexcel.save_as(array=data, dest_file_name="birth.xls")

Suppose we want to save previous used example 'birth.xls' as a csv file ::

   >>> import pyexcel
   >>> pyexcel.save_as(file_name="birth.xls", dest_file_name="birth.csv")

Again it is really simple. Let's verify what we have gotten:

   >>> sheet = pyexcel.get_sheet(file_name="birth.csv")
   >>> sheet
   birth.csv:
   +-------+--------+----------+
   | name  | weight | birth    |
   +-------+--------+----------+
   | Adam  | 3.4    | 03/02/15 |
   +-------+--------+----------+
   | Smith | 4.2    | 12/11/14 |
   +-------+--------+----------+

.. NOTE::

   Please note that csv(comma separate value) file is pure text file. Formula, charts, images and formatting in xls file will disappear no matter which transcoding tool you use. Hence, pyexcel is a quick alternative for this transcoding job.


.. _save_a_xls_as_a_xlsx:

How to open an xls file and save it as xlsx
----------------------------------------------------------------------

.. WARNING::

   Formula, charts, images and formatting in xls file will disappear as pyexcel does not support Formula, charts, images and formatting.


Let use previous example and save it as ods instead

   >>> import pyexcel
   >>> pyexcel.save_as(file_name="birth.xls",
   ...                 dest_file_name="birth.xlsx") # change the file extension

Again let's verify what we have gotten:

   >>> sheet = pyexcel.get_sheet(file_name="birth.xlsx")
   >>> sheet
   pyexcel_sheet1:
   +-------+--------+----------+
   | name  | weight | birth    |
   +-------+--------+----------+
   | Adam  | 3.4    | 03/02/15 |
   +-------+--------+----------+
   | Smith | 4.2    | 12/11/14 |
   +-------+--------+----------+

.. testcode::
   :hide:

   >>> session.close()
   >>> os.unlink('birth.xls')
   >>> os.unlink('birth.csv')
   >>> os.unlink('birth.xlsx')


How to open a xls multiple sheet excel book and save it as csv
----------------------------------------------------------------

Well, you write similar codes as before but you will need to use :meth:`~pyexcel.save_book_as` function.
