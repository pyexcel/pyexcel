
Stream APIs for big file : A set of two liners
================================================================================

When you are dealing with **BIG** excel files, you will want **pyexcel** to use
constant memory.

This section shows you how to get data from your **BIG** excel files and how to
export data to excel files in **two lines** at most, without eating all
your computer memory.


Two liners for get data from big excel files
--------------------------------------------------------------------------------

Get a list of dictionaries
********************************************************************************

.. testcode::
   :hide:

   >>> import os
   >>> import pyexcel as p
   >>> content="""
   ... Coffees,Serving Size,Caffeine (mg)
   ... Starbucks Coffee Blonde Roast,venti(20 oz),475
   ... Dunkin' Donuts Coffee with Turbo Shot,large(20 oz.),398
   ... Starbucks Coffee Pike Place Roast,grande(16 oz.),310
   ... Panera Coffee Light Roast,regular(16 oz.),300
   ... """.strip()
   >>> sheet = p.get_sheet(file_content=content, file_type='csv')
   >>> sheet.save_as("your_file.xls")



Suppose you want to process the following coffee data:

.. pyexcel-table::

   ---pyexcel:Huge list of coffeine drinks---
   Coffees,Serving Size,Caffeine (mg)
   Starbucks Coffee Blonde Roast,venti(20 oz),475
   Dunkin' Donuts Coffee with Turbo Shot,large(20 oz.),398
   Starbucks Coffee Pike Place Roast,grande(16 oz.),310
   Panera Coffee Light Roast,regular(16 oz.),300

Let's get a list of dictionary out from the xls file:

.. code-block:: python

   >>> records = p.iget_records(file_name="your_file.xls")

And let's check what do we have:

.. code-block:: python

   >>> for r in records:
   ...     print(f"{r['Serving Size']} of {r['Coffees']} has {r['Caffeine (mg)']} mg")
   venti(20 oz) of Starbucks Coffee Blonde Roast has 475 mg
   large(20 oz.) of Dunkin' Donuts Coffee with Turbo Shot has 398 mg
   grande(16 oz.) of Starbucks Coffee Pike Place Roast has 310 mg
   regular(16 oz.) of Panera Coffee Light Roast has 300 mg

Please do not forget the second line to close the opened file handle:

.. code-block:: python

   >>> p.free_resources()

Get two dimensional array
********************************************************************************

Instead, what if you have to use `pyexcel.get_array` to do the same:

.. code-block:: python

   >>> for row in p.iget_array(file_name="your_file.xls", start_row=1):
   ...     print(f"{row[1]} of {row[0]} has {row[2]} mg")
   venti(20 oz) of Starbucks Coffee Blonde Roast has 475 mg
   large(20 oz.) of Dunkin' Donuts Coffee with Turbo Shot has 398 mg
   grande(16 oz.) of Starbucks Coffee Pike Place Roast has 310 mg
   regular(16 oz.) of Panera Coffee Light Roast has 300 mg

Again, do not forget the second line:

.. code-block:: python

   >>> p.free_resources()

where `start_row` skips the header row.

Data export in one liners
---------------------------------------------

Export an array
**********************

Suppose you have the following array:

.. code-block:: python

   >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

And here is the code to save it as an excel file :

.. code-block:: python

   >>> p.isave_as(array=data, dest_file_name="example.xls")

But the following line is not required because the data source
are not file sources:

.. code-block:: python

   >>> # p.free_resources()

Let's verify it:

.. code-block:: python

    >>> p.get_sheet(file_name="example.xls")
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


And here is the code to save it as a csv file :

.. code-block:: python

   >>> p.isave_as(array=data,
   ...            dest_file_name="example.csv",
   ...            dest_delimiter=':')

Let's verify it:

.. code-block:: python

   >>> with open("example.csv") as f:
   ...     for line in f.readlines():
   ...         print(line.rstrip())
   ...
   1:2:3
   4:5:6
   7:8:9

Export a list of dictionaries
**********************************

.. code-block:: python

    >>> records = [
    ...     {"year": 1903, "country": "Germany", "speed": "206.7km/h"},
    ...     {"year": 1964, "country": "Japan", "speed": "210km/h"},
    ...     {"year": 2008, "country": "China", "speed": "350km/h"}
    ...     {"year": 2025, "country": "China", "speed": "400km/h"}    
    ... ]
    >>> p.isave_as(records=records, dest_file_name='high_speed_rail.xls')

Export a dictionary of single key value pair
********************************************************************************

.. code-block:: python

    >>> henley_on_thames_facts = {
    ...     "area": "5.58 square meters",
    ...     "population": "11,619",
    ...     "civial parish": "Henley-on-Thames",
    ...     "latitude": "51.536",
    ...     "longitude": "-0.898"
    ... }
    >>> p.isave_as(adict=henley_on_thames_facts, dest_file_name='henley.xlsx')

Export a dictionary of single dimensonal array
********************************************************************************

.. code-block:: python

    >>> ccs_insights = {
    ...     "year": ["2017", "2018", "2019", "2020", "2021"],
    ...     "smart phones": [1.53, 1.64, 1.74, 1.82, 1.90],
    ...     "feature phones": [0.46, 0.38, 0.30, 0.23, 0.17]
    ... }
    >>> p.isave_as(adict=ccs_insights, dest_file_name='ccs.csv')
    >>> p.free_resources()

Export a dictionary of two dimensional array as a book
********************************************************************************

Suppose you want to save the below dictionary to an excel file :

.. code-block:: python

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

Here is the code:

.. code-block:: python

   >>> p.isave_book_as(
   ...    bookdict=a_dictionary_of_two_dimensional_arrays,
   ...    dest_file_name="book.xls"
   ... )

If you want to preserve the order of sheets in your dictionary, you have to
pass on an ordered dictionary to the function itself. For example:

.. code-block:: python

   >>> from pyexcel._compact import OrderedDict
   >>> data = OrderedDict()
   >>> data.update({"Sheet 2": a_dictionary_of_two_dimensional_arrays['Sheet 2']})
   >>> data.update({"Sheet 1": a_dictionary_of_two_dimensional_arrays['Sheet 1']})
   >>> data.update({"Sheet 3": a_dictionary_of_two_dimensional_arrays['Sheet 3']})
   >>> p.isave_book_as(bookdict=data, dest_file_name="book.xls")
   >>> p.free_resources()

Let's verify its order:

.. code-block:: python

   >>> import json
   >>> book_dict = p.get_book_dict(file_name="book.xls")
   >>> for key, item in book_dict.items():
   ...     print(json.dumps({key: item}))
   {"Sheet 2": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]}
   {"Sheet 1": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}
   {"Sheet 3": [["O", "P", "Q"], [3, 2, 1], [4, 3, 2]]}

Please notice that "Sheet 2" is the first item in the *book_dict*, meaning the order of sheets are preserved.


File format transcoding on one line
-------------------------------------------

.. note::

   Please note that the following file transcoding could be with zero line. Please
   install pyexcel-cli and you will do the transcode in one command. No need to
   open your editor, save the problem, then python run.


.. testcode::
   :hide:

   >>> import datetime
   >>> data = [
   ...    ["name", "weight", "birth"],
   ...    ["Adam", 3.4, datetime.date(2015, 2, 3)],
   ...    ["Smith", 4.2, datetime.date(2014, 11, 12)]
   ... ]
   >>> p.isave_as(array=data, dest_file_name="birth.xls")


The following code does a simple file format transcoding from xls to csv:

.. code-block:: python

   >>> import pyexcel
   >>> p.save_as(file_name="birth.xls", dest_file_name="birth.csv")

Again it is really simple. Let's verify what we have gotten:

.. code-block:: python

   >>> sheet = p.get_sheet(file_name="birth.csv")
   >>> sheet
   birth.csv:
   +-------+--------+----------+
   | name  | weight | birth    |
   +-------+--------+----------+
   | Adam  | 3.4    | 03/02/15 |
   +-------+--------+----------+
   | Smith | 4.2    | 12/11/14 |
   +-------+--------+----------+

.. note::

   Please note that csv(comma separate value) file is pure text file. Formula, charts, images and formatting in xls file will disappear no matter which transcoding tool you use. Hence, pyexcel is a quick alternative for this transcoding job.


Let use previous example and save it as xlsx instead

.. code-block:: python

   >>> import pyexcel
   >>> p.isave_as(file_name="birth.xls",
   ...            dest_file_name="birth.xlsx") # change the file extension

Again let's verify what we have gotten:

.. code-block:: python

   >>> sheet = p.get_sheet(file_name="birth.xlsx")
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

   >>> import os
   >>> os.unlink('ccs.csv')
   >>> os.unlink('book.xls')
