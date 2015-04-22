Signature functions
====================

Import data into Python
---------------------------

This library provides one application programming interface to read data from one of the following data sources:

   * physical file
   * memory file
   * SQLAlchemy table
   * Django Model
   * Python data stuctures: dictionary, records and array

and to transform them into one of the data structures:

   * two dimensinal array
   * a dictionary of one dimensional arrays
   * a list of dictionaries
   * a dictionary of two dimensional arrays
   * a :class:`~pyexcel.Sheet`
   * a :class:`~pyexcel.Book`


Four data access functions
++++++++++++++++++++++++++++

It is believed that once a Python developer could easily operate on list, dictionary and various mixture of both. This library provides four
module level functions to help you obtain excel data in those formats. Please refer to "A list of module level functions",
the first three functions operates on any one sheet from an excel book and the fourth one returns all data in all sheets in an excel book.

.. table:: A list of module level functions

   =============================== ======================================= ================================ 
   Functions                       Psudo name                              Python name                      
   =============================== ======================================= ================================ 
   :meth:`~pyexcel.get_array`      two dimensional array                   a list of lists                 
   :meth:`~pyexcel.get_dict`       a dictionary of one dimensional arrays  an ordered dictionary of lists           
   :meth:`~pyexcel.get_records`    a list of dictionaries                  a list of dictionaries           
   :meth:`~pyexcel.get_book_dict`  a dictionary of two dimensional arrays  a dictionary of lists of lists      
   =============================== ======================================= ================================

How to get an array from an excel sheet
-----------------------------------------

Suppose you have a csv, xls, xlsx file as the following:

= = =
1 2 3
4 5 6
7 8 9
= = =

.. testcode::
   :hide:

   >>> import pyexcel as pe
   >>> import pyexcel.ext.xls   
   >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
   >>> s = pe.Sheet(data)
   >>> s.save_as("example.xls")

The following code will give you the data in json::

    >>> import pyexcel
	>>> import pyexcel.ext.xls
    >>> # "example.csv","example.xlsx","example.xlsm"
    >>> my_array = pyexcel.get_array(file_name="example.xls")
    >>> my_array
    [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example.xls")


How to get an array from an excel sheet
-----------------------------------------

Suppose you have a csv, xls, xlsx file as the following:

======== ========= ========
Column 1 Column 2  Column 3
======== ========= ========
1        4         7
2        5         8
3        6         9
======== ========= ========

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
   >>> import pyexcel.ext.xls
   >>> from pyexcel._compact import OrderedDict
   >>> my_dict = pyexcel.get_dict(file_name="example_series.xls", name_columns_by_row=0)
   >>> isinstance(my_dict, OrderedDict)
   True
   >>> for key, values in my_dict.items():
   ...     print({key: values})
   {'Column 1': [1.0, 4.0, 7.0]}
   {'Column 2': [2.0, 5.0, 8.0]}
   {'Column 3': [3.0, 6.0, 9.0]}

Please note that my_dict is an OrderedDict.

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example_series.xls")


How to get so called 'records' from an excel sheet
---------------------------------------------------

.. testcode::
   :hide:

   >>> import pyexcel as pe
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

Here are the example code::
   
   >>> import pyexcel
   >>> import pyexcel.ext.xls # import it to handle xls file
   >>> records = pyexcel.get_records(file_name="your_file.xls")
   >>> for record in records:
   ...     print("%s is aged at %d" % (record['Name'], record['Age']))
   Adam is aged at 28
   Beatrice is aged at 29
   Ceri is aged at 30
   Dean is aged at 26

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("your_file.xls")



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

.. table:: Sheet 1

    = = =
    1 2 3
    4 5 6
    7 8 9
    = = =

.. table:: Sheet 2

    = = =
    X Y Z
    1 2 3
    4 5 6
    = = =

.. table:: Sheet 3

    = = =
    O P Q
    3 2 1
    4 3 2
    = = =

Here is the code to obtain those sheets as a single dictionary::

   >>> import pyexcel
   >>> import pyexcel.ext.xls # import it to handle xls file
   >>> book_dict = pyexcel.get_book_dict(file_name="book.xls")
   >>> isinstance(book_dict, OrderedDict)
   True
   >>> for key, values in book_dict.items():
   ...     print("{%s:%s}" % (key, values))
   {Sheet 1:[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]}
   {Sheet 2:[[u'X', u'Y', u'Z'], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}
   {Sheet 3:[[u'O', u'P', u'Q'], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]]}

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("book.xls")


Two native functions
++++++++++++++++++++++

In cases where the excel data needs a bit of formatting, a pyexcel user got two choices: one is diy, the other is to use :class:`~pyexcel.Sheet`
and :class:`~pyexcel.Book` to do them.

=============================== ================================ 
Functions                       Python name                      
=============================== ================================ 
:meth:`~pyexcel.get_sheet`      :class:`~pyexcel.Sheet`
:meth:`~pyexcel.get_book`       :class:`~pyexcel.Book`
=============================== ================================ 

Export data from Python
-------------------------

This library provides one application programming interface to transform them into one of the data structures:

   * two dimensinal array
   * a (ordered) dictionary of one dimensional arrays
   * a list of dictionaries
   * a dictionary of two dimensional arrays
   * a :class:`~pyexcel.Sheet`
   * a :class:`~pyexcel.Book`

and write to one of the following data sources:

   * physical file
   * memory file
   * SQLAlchemy table
   * Django Model
   * Python data stuctures: dictionary, records and array

How to save an python array as an excel file
---------------------------------------------

Suppose you have the following array::

   >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

And here is the code to save it as an excel file ::

   >>> import pyexcel
   >>> import pyexcel.ext.xls   
   >>> pyexcel.save_as(array=data, dest_file_name="example.xls")

Let's verify it::

   >>> pyexcel.get_sheet(file_name="example.xls")
   Sheet Name: pyexcel_sheet1
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



How to save a dictionary of two dimensional array as an excel file
--------------------------------------------------------------------


Here are the two functions:

=============================== ================================ 
Functions                       Python name                      
=============================== ================================ 
:meth:`~pyexcel.save_as`        :class:`~pyexcel.Sheet`
:meth:`~pyexcel.save_book_as`   :class:`~pyexcel.Book`
=============================== ================================ 


Data transportation/transcoding
----------------------------------

Based the capability of this library, it is capable of transporting your data in between any of these data sources:

   * physical file
   * memory file
   * SQLAlchemy table
   * Django Model
   * Python data stuctures: dictionary, records and array

