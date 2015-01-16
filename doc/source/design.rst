Excel data
================================

Data models and data structures
--------------------------------
When dealing with excel files, there are three primary objects: **cell**, **sheet** and **book**.
A book contains one or more sheets and a sheet is consisted of a sheet
name and a two dimensional array of cells. Although a sheet can contain charts and a cell can have
formular, styling properties, this library ignores them and pay attention to the data in the cell
and its data type. So, in the context of this library, the definition of those three concepts are:

========= ======================================================== =======================
concept   definition                                               pyexcel data model
========= ======================================================== =======================
a cell    is a data unit                                           a Python data type
a sheet   is a named two dimensional array of data units           :class:`~pyexcel.Sheet`
a book    is a dictionary of two dimensional array of data units.  :class:`~pyexcel.Book`
========= ======================================================== =======================

Data source
-------------

The most popular data source is an excel file. Libre Offcie/Microsoft Excel could easily
generate an new excel file of desired format. Besides a physical file, this library
recognizes additional three additional sources:

#. Excel files in computer memory. For example when a file was uploaded to a Python server for
   information processing, if it is relatively small, it will be stored in memory.
#. Database tables. For example, a client would like to have a snapshot of some database table in
   an excel file and ask it to be sent to him.
#. Python structures. For example, a developer may have scrapped a site and hence stored data
   in Python array or dictionary. He may want to save those information as a file.

Data format
-------------

This library and its plugins support most of the frequently used excel file formats. 

============ ======================================================= =============
file format  defintion                                               Single Sheet
============ ======================================================= =============
csv          comma separated values                                  Yes
tsv          tab separated values                                    Yes
csvz         a zip file that contains one or many csv files
tsvz         a zip file that contains one or many tsv files
xls          
xlsx
xlsm
ods          open document spreadsheet
json         java script object notation
============ ======================================================= =============
See also :ref:`a-map-of-plugins-and-file-formats`.

Data transformation
----------------------

Quite often, a developer would like to have the excel data in a Python data structures. This library
supports the :ref:`conversions from<conversion-from>` previous three data source to the following
list of data strcutures, and :ref:`vice versa<conversion-to>`.

.. _a-list-of-data-structures:
.. table:: A list of supported data structures

   ======================================= ================================ =========================
   Psudo name                              Python name                      Related model
   ======================================= ================================ =========================
   two dimensional array                   a list of lists                  :class:`~pyexcel.Sheet`
   a dictionary of one dimensional arrays  a dictionary of lists            :class:`~pyexcel.Sheet`
   a list of dictionaries                  a list of dictionaries           :class:`~pyexcel.Sheet`
   a dictionary of two dimensional arrays  a dictionary of lists of lists   :class:`~pyexcel.Book`
   ======================================= ================================ =========================

Examples::

    >>> two_dimensional_list = [
    ...    [1, 2, 3, 4],
    ...    [5, 6, 7, 8],
    ...    [9, 10, 11, 12],
    ... ]
    >>> a_dictionary_of_one_dimensional_arrays = {
    ...     "Column 1": [1, 2, 3, 4],
    ...     "Column 2": [5, 6, 7, 8],
    ...     "Column 3": [9, 10, 11, 12],
    ... }
    >>> a_list_of_dictionaries = [
    ...     {
    ...         "Name": Adam,
    ...         "Age": 28
    ...     },
    ...     {
    ...         "Name": Beatrice,
    ...         "Age": 29
    ...     },
    ...     {
    ...         "Name": Ceri,
    ...         "Age": 30
    ...     },
    ...     {
    ...         "Name": Dean,
    ...         "Age": 26
    ...     }
    ... ]
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


Data manipulations
--------------------

The main operation on a cell involves :ref:`cell access<access-to-cell>`,
:ref:`formatting<formatting>` and :ref:`cleansing<cleansing>`. The main operation on a sheet
involves the group access to a row or a column, data filtering and data transformation. The
main operation in a book is obtain access to individual sheets.
