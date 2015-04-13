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

