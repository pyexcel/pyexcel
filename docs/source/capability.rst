Signature functions
====================

Import data into Python
---------------------------

This library provides one application programming interface to read data from one of the following data sources:

   * physical file
   * memory file
   * SQLAlchemy table
   * Django Model
   * Python data structures: dictionary, records and array

and to transform them into one of the data structures:

   * two dimensional array
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
   Functions                       Name                                    Python name                      
   =============================== ======================================= ================================ 
   :meth:`~pyexcel.get_array`      two dimensional array                   a list of lists                 
   :meth:`~pyexcel.get_dict`       a dictionary of one dimensional arrays  an ordered dictionary of lists           
   :meth:`~pyexcel.get_records`    a list of dictionaries                  a list of dictionaries           
   :meth:`~pyexcel.get_book_dict`  a dictionary of two dimensional arrays  a dictionary of lists of lists      
   =============================== ======================================= ================================

See also:

* :ref:`get_an_array_from_an_excel_sheet`
* :ref:`get_a_dict_from_an_excel_sheet`
* :ref:`get_records_from_an_excel_sheet`
* :ref:`get_an_book_dict_from_an_excel_book`

The following two variants of the data access function use generator and should work well with big data files

.. table:: A list of variant functions

   =============================== ======================================= ================================ 
   Functions                       Name                                    Python name                      
   =============================== ======================================= ================================ 
   :meth:`~pyexcel.iget_array`     a memory efficient two dimensional      a generator of a list of lists
		                           array
   :meth:`~pyexcel.iget_records`   a memory efficient list                 a generator of
                                   list of dictionaries                    a list of dictionaries
   =============================== ======================================= ================================


Two native functions
++++++++++++++++++++++

In cases where the excel data needs custom manipulations, a pyexcel user got a few choices: one is to use :class:`~pyexcel.Sheet`
and :class:`~pyexcel.Book`, the other is to look for more sophisticated ones:

* Pandas, for numerical analysis
* Do-it-yourself

=============================== ================================ 
Functions                       Returns                      
=============================== ================================ 
:meth:`~pyexcel.get_sheet`      :class:`~pyexcel.Sheet`
:meth:`~pyexcel.get_book`       :class:`~pyexcel.Book`
=============================== ================================ 

For all six functions, you can pass on the same command parameters while the return value is what the function says.


Export data from Python
-------------------------

This library provides one application programming interface to transform them into one of the data structures:

   * two dimensional array
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
   * Python data structures: dictionary, records and array


Here are the two functions:

=============================== =================================
Functions                       Description
=============================== ================================= 
:meth:`~pyexcel.save_as`        Works well with single sheet file
:meth:`~pyexcel.isave_as`       Works well with big data files	  
:meth:`~pyexcel.save_book_as`   Works with multiple sheet file
	                            and big data files
:meth:`~pyexcel.isave_book_as`  Works with multiple sheet file
	                            and big data files
=============================== =================================

If you would only use these two functions to do format transcoding, you may enjoy a
speed boost using :meth:`~pyexcel.isave_as` and :meth:`~pyexcel.isave_book_as`,
because they use `yield` keyword and minimize memory footprint.
:meth:`~pyexcel.save_as` and :meth:`~pyexcel.save_book_as` reads all data into
memory and **will make all rows the same width**.


See also:

* :ref:`save_an_array_to_an_excel_sheet`
* :ref:`save_an_book_dict_to_an_excel_book`
* :ref:`save_an_array_to_a_csv_with_custom_delimiter`

Data transportation/transcoding
----------------------------------

Based the capability of this library, it is capable of transporting your data in between any of these data sources:

   * physical file
   * memory file
   * SQLAlchemy table
   * Django Model
   * Python data structures: dictionary, records and array

See also:

* :ref:`import_excel_sheet_into_a_database_table`
* :ref:`save_a_xls_as_a_xlsx`
* :ref:`save_a_xls_as_a_csv`
