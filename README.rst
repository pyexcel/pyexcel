================================================================================
pyexcel - Let you focus on data, instead of file formats
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/chfw

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel-mobans/master/images/awesome-badge.svg
   :target: https://awesome-python.com/#specific-formats-processing

.. image:: https://github.com/pyexcel/pyexcel/workflows/run_tests/badge.svg
   :target: http://github.com/pyexcel/pyexcel/actions

.. image:: https://codecov.io/gh/pyexcel/pyexcel/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pyexcel/pyexcel

.. image:: https://badge.fury.io/py/pyexcel.svg
   :target: https://pypi.org/project/pyexcel

.. image:: https://anaconda.org/conda-forge/pyexcel/badges/version.svg
   :target: https://anaconda.org/conda-forge/pyexcel

.. image:: https://pepy.tech/badge/pyexcel/month
   :target: https://pepy.tech/project/pyexcel

.. image:: https://anaconda.org/conda-forge/pyexcel/badges/downloads.svg
   :target: https://anaconda.org/conda-forge/pyexcel

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/pyexcel/Lobby

.. image:: https://img.shields.io/static/v1?label=continuous%20templating&message=%E6%A8%A1%E7%89%88%E6%9B%B4%E6%96%B0&color=blue&style=flat-square
    :target: https://moban.readthedocs.io/en/latest/#at-scale-continous-templating-for-open-source-projects

.. image:: https://img.shields.io/static/v1?label=coding%20style&message=black&color=black&style=flat-square
    :target: https://github.com/psf/black
.. image:: https://readthedocs.org/projects/pyexcel/badge/?version=latest
   :target: http://pyexcel.readthedocs.org/en/latest/

Support the project
================================================================================

If your company has embedded pyexcel and its components into a revenue generating
product, please support me on github, `patreon <https://www.patreon.com/bePatron?u=5537627>`_
or `bounty source <https://salt.bountysource.com/teams/chfw-pyexcel>`_ to maintain
the project and develop it further.

If you are an individual, you are welcome to support me too and for however long
you feel like. As my backer, you will receive
`early access to pyexcel related contents <https://www.patreon.com/pyexcel/posts>`_.

And your issues will get prioritized if you would like to become my patreon as `pyexcel pro user`.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting posts.


Known constraints
==================

Fonts, colors and charts are not supported.

Nor to read password protected xls, xlsx and ods files.

Introduction
================================================================================

Feature Highlights
===================

.. table:: A list of supported file formats

    ============ =======================================================
    file format  definition
    ============ =======================================================
    csv          comma separated values
    tsv          tab separated values
    csvz         a zip file that contains one or many csv files
    tsvz         a zip file that contains one or many tsv files
    xls          a spreadsheet file format created by
                 MS-Excel 97-2003 
    xlsx         MS-Excel Extensions to the Office Open XML
                 SpreadsheetML File Format.
    xlsm         an MS-Excel Macro-Enabled Workbook file
    ods          open document spreadsheet
    fods         flat open document spreadsheet
    json         java script object notation
    html         html table of the data structure
    simple       simple presentation
    rst          rStructured Text presentation of the data
    mediawiki    media wiki table
    ============ =======================================================


.. image:: https://github.com/pyexcel/pyexcel/raw/dev/docs/source/_static/images/architecture.svg


1. One application programming interface(API) to handle multiple data sources:

   * physical file
   * memory file
   * SQLAlchemy table
   * Django Model
   * Python data structures: dictionary, records and array

2. One API to read and write data in various excel file formats.
3. For large data sets, data streaming are supported. A genenerator can be returned to you. Checkout iget_records, iget_array, isave_as and isave_book_as.




Installation
================================================================================

You can install pyexcel via pip:

.. code-block:: bash

    $ pip install pyexcel


or clone it and install it:

.. code-block:: bash

    $ git clone https://github.com/pyexcel/pyexcel.git
    $ cd pyexcel
    $ python setup.py install



One liners
================================================================================

This section shows you how to get data from your excel files and how to
export data to excel files in **one line**

Read from the excel files
--------------------------------------------------------------------------------

Get a list of dictionaries
********************************************************************************


Suppose you want to process the following coffee data (data source `coffee chart <https://cspinet.org/eating-healthy/ingredients-of-concern/caffeine-chart>`_ on the center for science in the public interest):


Top 5 coffeine drinks:

=====================================  ===============  =============
Coffees                                Serving Size     Caffeine (mg)
Starbucks Coffee Blonde Roast          venti(20 oz)     475
Dunkin' Donuts Coffee with Turbo Shot  large(20 oz.)    398
Starbucks Coffee Pike Place Roast      grande(16 oz.)   310
Panera Coffee Light Roast              regular(16 oz.)  300
=====================================  ===============  =============


Let's get a list of dictionary out from the xls file:

.. code-block:: python

   >>> records = p.get_records(file_name="your_file.xls")

And let's check what do we have:

.. code-block:: python

   >>> for r in records:
   ...     print(f"{r['Serving Size']} of {r['Coffees']} has {r['Caffeine (mg)']} mg")
   venti(20 oz) of Starbucks Coffee Blonde Roast has 475 mg
   large(20 oz.) of Dunkin' Donuts Coffee with Turbo Shot has 398 mg
   grande(16 oz.) of Starbucks Coffee Pike Place Roast has 310 mg
   regular(16 oz.) of Panera Coffee Light Roast has 300 mg


Get two dimensional array
********************************************************************************

Instead, what if you have to use `pyexcel.get_array` to do the same:

.. code-block:: python

   >>> for row in p.get_array(file_name="your_file.xls", start_row=1):
   ...     print(f"{row[1]} of {row[0]} has {row[2]} mg")
   venti(20 oz) of Starbucks Coffee Blonde Roast has 475 mg
   large(20 oz.) of Dunkin' Donuts Coffee with Turbo Shot has 398 mg
   grande(16 oz.) of Starbucks Coffee Pike Place Roast has 310 mg
   regular(16 oz.) of Panera Coffee Light Roast has 300 mg


where `start_row` skips the header row.


Get a dictionary
********************************************************************************

You can get a dictionary too:

Now let's get a dictionary out from the spreadsheet:

.. code-block:: python

   >>> my_dict = p.get_dict(file_name="your_file.xls", name_columns_by_row=0)

And check what do we have:

.. code-block:: python

   >>> from pyexcel._compact import OrderedDict
   >>> isinstance(my_dict, OrderedDict)
   True
   >>> for key, values in my_dict.items():
   ...     print(key + " : " + ','.join([str(item) for item in values]))
   Coffees : Starbucks Coffee Blonde Roast,Dunkin' Donuts Coffee with Turbo Shot,Starbucks Coffee Pike Place Roast,Panera Coffee Light Roast
   Serving Size : venti(20 oz),large(20 oz.),grande(16 oz.),regular(16 oz.)
   Caffeine (mg) : 475,398,310,300

Please note that my_dict is an OrderedDict.

Get a dictionary of two dimensional array
********************************************************************************


Suppose you have a multiple sheet book as the following:


pyexcel:Sheet 1:

=====================  =  =
1                      2  3
4                      5  6
7                      8  9
=====================  =  =

pyexcel:Sheet 2:

=====================  =  =
X                      Y  Z
1                      2  3
4                      5  6
=====================  =  =

pyexcel:Sheet 3:

=====================  =  =
O                      P  Q
3                      2  1
4                      3  2
=====================  =  =


Here is the code to obtain those sheets as a single dictionary:

.. code-block:: python

   >>> book_dict = p.get_book_dict(file_name="book.xls")

And check:

.. code-block:: python

   >>> isinstance(book_dict, OrderedDict)
   True
   >>> import json
   >>> for key, item in book_dict.items():
   ...     print(json.dumps({key: item}))
   {"Sheet 1": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}
   {"Sheet 2": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]}
   {"Sheet 3": [["O", "P", "Q"], [3, 2, 1], [4, 3, 2]]}


Write data
---------------------------------------------

Export an array
**********************

Suppose you have the following array:

.. code-block:: python

   >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

And here is the code to save it as an excel file :

.. code-block:: python

   >>> p.save_as(array=data, dest_file_name="example.xls")

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


And here is the code to save it as a csv file :

.. code-block:: python

   >>> p.save_as(array=data,
   ...           dest_file_name="example.csv",
   ...           dest_delimiter=':')

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
    ... ]
    >>> p.save_as(records=records, dest_file_name='high_speed_rail.xls')


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
    >>> p.save_as(adict=henley_on_thames_facts, dest_file_name='henley.xlsx')


Export a dictionary of single dimensonal array
********************************************************************************

.. code-block:: python

    >>> ccs_insights = {
    ...     "year": ["2017", "2018", "2019", "2020", "2021"],
    ...     "smart phones": [1.53, 1.64, 1.74, 1.82, 1.90],
    ...     "feature phones": [0.46, 0.38, 0.30, 0.23, 0.17]
    ... }
    >>> p.save_as(adict=ccs_insights, dest_file_name='ccs.csv')


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

   >>> p.save_book_as(
   ...    bookdict=a_dictionary_of_two_dimensional_arrays,
   ...    dest_file_name="book.xls"
   ... )

If you want to preserve the order of sheets in your dictionary, you have to
pass on an ordered dictionary to the function itself. For example:

.. code-block:: python

   >>> data = OrderedDict()
   >>> data.update({"Sheet 2": a_dictionary_of_two_dimensional_arrays['Sheet 2']})
   >>> data.update({"Sheet 1": a_dictionary_of_two_dimensional_arrays['Sheet 1']})
   >>> data.update({"Sheet 3": a_dictionary_of_two_dimensional_arrays['Sheet 3']})
   >>> p.save_book_as(bookdict=data, dest_file_name="book.xls")

Let's verify its order:

.. code-block:: python

   >>> book_dict = p.get_book_dict(file_name="book.xls")
   >>> for key, item in book_dict.items():
   ...     print(json.dumps({key: item}))
   {"Sheet 2": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]}
   {"Sheet 1": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}
   {"Sheet 3": [["O", "P", "Q"], [3, 2, 1], [4, 3, 2]]}

Please notice that "Sheet 2" is the first item in the *book_dict*, meaning the order of sheets are preserved.


Transcoding
-------------------------------------------

.. note::

   Please note that `pyexcel-cli` can perform file transcoding at command line.
   No need to open your editor, save the problem, then python run.


The following code does a simple file format transcoding from xls to csv:

.. code-block:: python

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

.. NOTE::

   Please note that csv(comma separate value) file is pure text file. Formula, charts, images and formatting in xls file will disappear no matter which transcoding tool you use. Hence, pyexcel is a quick alternative for this transcoding job.


Let use previous example and save it as xlsx instead

.. code-block:: python

   >>> p.save_as(file_name="birth.xls",
   ...           dest_file_name="birth.xlsx") # change the file extension

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


Excel book merge and split operation in one line
--------------------------------------------------------------------------------

Merge all excel files in directory into  a book where each file become a sheet
********************************************************************************

The following code will merge every excel files into one file, say "output.xls":

.. code-block:: python

    from pyexcel.cookbook import merge_all_to_a_book
    import glob


    merge_all_to_a_book(glob.glob("your_csv_directory\*.csv"), "output.xls")

You can mix and match with other excel formats: xls, xlsm and ods. For example, if you are sure you have only xls, xlsm, xlsx, ods and csv files in `your_excel_file_directory`, you can do the following:

.. code-block:: python

    from pyexcel.cookbook import merge_all_to_a_book
    import glob


    merge_all_to_a_book(glob.glob("your_excel_file_directory\*.*"), "output.xls")

Split a book into single sheet files
****************************************


Suppose you have many sheets in a work book and you would like to separate each into a single sheet excel file. You can easily do this:

.. code-block:: python

   >>> from pyexcel.cookbook import split_a_book
   >>> split_a_book("megabook.xls", "output.xls")
   >>> import glob
   >>> outputfiles = glob.glob("*_output.xls")
   >>> for file in sorted(outputfiles):
   ...     print(file)
   ...
   Sheet 1_output.xls
   Sheet 2_output.xls
   Sheet 3_output.xls

for the output file, you can specify any of the supported formats


Extract just one sheet from a book
*************************************


Suppose you just want to extract one sheet from many sheets that exists in a work book and you would like to separate it into a single sheet excel file. You can easily do this:

.. code-block:: python

    >>> from pyexcel.cookbook import extract_a_sheet_from_a_book
    >>> extract_a_sheet_from_a_book("megabook.xls", "Sheet 1", "output.xls")
    >>> if os.path.exists("Sheet 1_output.xls"):
    ...     print("Sheet 1_output.xls exists")
    ...
    Sheet 1_output.xls exists

for the output file, you can specify any of the supported formats


Hidden feature: partial read
===============================================

Most pyexcel users do not know, but other library users were requesting `the similar features <https://github.com/jazzband/tablib/issues/467>`_


When you are dealing with huge amount of data, e.g. 64GB, obviously you would not
like to fill up your memory with those data. What you may want to do is, record
data from Nth line, take M records and stop. And you only want to use your memory
for the M records, not for beginning part nor for the tail part.

Hence partial read feature is developed to read partial data into memory for
processing. 

You can paginate by row, by column and by both, hence you dictate what portion of the
data to read back. But remember only row limit features help you save memory. Let's
you use this feature to record data from Nth column, take M number of columns and skip
the rest. You are not going to reduce your memory footprint.

Why did not I see above benefit?
--------------------------------------------------------------------------------

This feature depends heavily on the implementation details.

`pyexcel-xls`_ (xlrd), `pyexcel-xlsx`_ (openpyxl), `pyexcel-ods`_ (odfpy) and
`pyexcel-ods3`_ (pyexcel-ezodf) will read all data into memory. Because xls,
xlsx and ods file are effective a zipped folder, all four will unzip the folder
and read the content in xml format in **full**, so as to make sense of all details.

Hence, during the partial data is been returned, the memory consumption won't
differ from reading the whole data back. Only after the partial
data is returned, the memory comsumption curve shall jump the cliff. So pagination
code here only limits the data returned to your program.

With that said, `pyexcel-xlsxr`_, `pyexcel-odsr`_ and `pyexcel-htmlr`_ DOES read
partial data into memory. Those three are implemented in such a way that they
consume the xml(html) when needed. When they have read designated portion of the
data, they stop, even if they are half way through.

In addition, pyexcel's csv readers can read partial data into memory too.


Let's assume the following file is a huge csv file:

.. code-block:: python

   >>> import datetime
   >>> import pyexcel as pe
   >>> data = [
   ...     [1, 21, 31],
   ...     [2, 22, 32],
   ...     [3, 23, 33],
   ...     [4, 24, 34],
   ...     [5, 25, 35],
   ...     [6, 26, 36]
   ... ]
   >>> pe.save_as(array=data, dest_file_name="your_file.csv")


And let's pretend to read partial data:


.. code-block:: python

   >>> pe.get_sheet(file_name="your_file.csv", start_row=2, row_limit=3)
   your_file.csv:
   +---+----+----+
   | 3 | 23 | 33 |
   +---+----+----+
   | 4 | 24 | 34 |
   +---+----+----+
   | 5 | 25 | 35 |
   +---+----+----+

And you could as well do the same for columns:

.. code-block:: python

   >>> pe.get_sheet(file_name="your_file.csv", start_column=1, column_limit=2)
   your_file.csv:
   +----+----+
   | 21 | 31 |
   +----+----+
   | 22 | 32 |
   +----+----+
   | 23 | 33 |
   +----+----+
   | 24 | 34 |
   +----+----+
   | 25 | 35 |
   +----+----+
   | 26 | 36 |
   +----+----+

Obvious, you could do both at the same time:

.. code-block:: python

   >>> pe.get_sheet(file_name="your_file.csv",
   ...     start_row=2, row_limit=3,
   ...     start_column=1, column_limit=2)
   your_file.csv:
   +----+----+
   | 23 | 33 |
   +----+----+
   | 24 | 34 |
   +----+----+
   | 25 | 35 |
   +----+----+


The pagination support is available across all pyexcel plugins.

.. note::

   No column pagination support for query sets as data source. 


Formatting while transcoding a big data file
--------------------------------------------------------------------------------

If you are transcoding a big data set, conventional formatting method would not
help unless a on-demand free RAM is available. However, there is a way to minimize
the memory footprint of pyexcel while the formatting is performed.

Let's continue from previous example. Suppose we want to transcode "your_file.csv"
to "your_file.xls" but increase each element by 1.

What we can do is to define a row renderer function as the following:

.. code-block:: python

   >>> def increment_by_one(row):
   ...     for element in row:
   ...         yield element + 1

Then pass it onto save_as function using row_renderer:

.. code-block:: python

   >>> pe.isave_as(file_name="your_file.csv",
   ...             row_renderer=increment_by_one,
   ...             dest_file_name="your_file.xlsx")


.. note::

   If the data content is from a generator, isave_as has to be used.
   
We can verify if it was done correctly:

.. code-block:: python

   >>> pe.get_sheet(file_name="your_file.xlsx")
   your_file.csv:
   +---+----+----+
   | 2 | 22 | 32 |
   +---+----+----+
   | 3 | 23 | 33 |
   +---+----+----+
   | 4 | 24 | 34 |
   +---+----+----+
   | 5 | 25 | 35 |
   +---+----+----+
   | 6 | 26 | 36 |
   +---+----+----+
   | 7 | 27 | 37 |
   +---+----+----+


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



Suppose you want to process the following coffee data again:

Top 5 coffeine drinks:

=====================================  ===============  =============
Coffees                                Serving Size     Caffeine (mg)
Starbucks Coffee Blonde Roast          venti(20 oz)     475
Dunkin' Donuts Coffee with Turbo Shot  large(20 oz.)    398
Starbucks Coffee Pike Place Roast      grande(16 oz.)   310
Panera Coffee Light Roast              regular(16 oz.)  300
=====================================  ===============  =============


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

Please do not forgot the second line to close the opened file handle:

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

Again, do not forgot the second line:

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


Available Plugins
=================

.. _file-format-list:
.. _a-map-of-plugins-and-file-formats:

.. table:: A list of file formats supported by external plugins

   ======================== ======================= =================
   Package name              Supported file formats  Dependencies
   ======================== ======================= =================
   `pyexcel-io`_            csv, csvz [#f1]_, tsv,
                            tsvz [#f2]_
   `pyexcel-xls`_           xls, xlsx(read only),   `xlrd`_,
                            xlsm(read only)         `xlwt`_
   `pyexcel-xlsx`_          xlsx                    `openpyxl`_
   `pyexcel-ods3`_          ods                     `pyexcel-ezodf`_,
                                                    lxml
   `pyexcel-ods`_           ods                     `odfpy`_
   ======================== ======================= =================

.. table:: Dedicated file reader and writers

   ======================== ======================= =================
   Package name              Supported file formats  Dependencies
   ======================== ======================= =================
   `pyexcel-xlsxw`_         xlsx(write only)        `XlsxWriter`_
   `pyexcel-libxlsxw`_      xlsx(write only)        `libxlsxwriter`_
   `pyexcel-xlsxr`_         xlsx(read only)         lxml
   `pyexcel-xlsbr`_         xlsb(read only)         pyxlsb
   `pyexcel-odsr`_          read only for ods, fods lxml
   `pyexcel-odsw`_          write only for ods      loxun
   `pyexcel-htmlr`_         html(read only)         lxml,html5lib
   `pyexcel-pdfr`_          pdf(read only)          camelot
   ======================== ======================= =================


Plugin shopping guide
------------------------

Since 2020, all pyexcel-io plugins have dropped the support for python version
lower than 3.6. If you want to use any python verions, please use pyexcel-io
and its plugins version lower than 0.6.0.


Except csv files, xls, xlsx and ods files are a zip of a folder containing a lot of
xml files

The dedicated readers for excel files can stream read


In order to manage the list of plugins installed, you need to use pip to add or remove
a plugin. When you use virtualenv, you can have different plugins per virtual
environment. In the situation where you have multiple plugins that does the same thing
in your environment, you need to tell pyexcel which plugin to use per function call.
For example, pyexcel-ods and pyexcel-odsr, and you want to get_array to use pyexcel-odsr.
You need to append get_array(..., library='pyexcel-odsr').



.. _pyexcel-io: https://github.com/pyexcel/pyexcel-io
.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-odsr: https://github.com/pyexcel/pyexcel-odsr
.. _pyexcel-odsw: https://github.com/pyexcel/pyexcel-odsw
.. _pyexcel-pdfr: https://github.com/pyexcel/pyexcel-pdfr

.. _pyexcel-xlsxw: https://github.com/pyexcel/pyexcel-xlsxw
.. _pyexcel-libxlsxw: https://github.com/pyexcel/pyexcel-libxlsxw
.. _pyexcel-xlsxr: https://github.com/pyexcel/pyexcel-xlsxr
.. _pyexcel-xlsbr: https://github.com/pyexcel/pyexcel-xlsbr
.. _pyexcel-htmlr: https://github.com/pyexcel/pyexcel-htmlr

.. _xlrd: https://github.com/python-excel/xlrd
.. _xlwt: https://github.com/python-excel/xlwt
.. _openpyxl: https://bitbucket.org/openpyxl/openpyxl
.. _XlsxWriter: https://github.com/jmcnamara/XlsxWriter
.. _pyexcel-ezodf: https://github.com/pyexcel/pyexcel-ezodf
.. _odfpy: https://github.com/eea/odfpy
.. _libxlsxwriter: http://libxlsxwriter.github.io/getting_started.html

.. table:: Other data renderers

   ======================== ======================= ================= ==================
   Package name              Supported file formats  Dependencies     Python versions
   ======================== ======================= ================= ==================
   `pyexcel-text`_          write only:rst,         `tabulate`_       2.6, 2.7, 3.3, 3.4
                            mediawiki, html,                          3.5, 3.6, pypy
                            latex, grid, pipe,
                            orgtbl, plain simple
                            read only: ndjson
                            r/w: json
   `pyexcel-handsontable`_  handsontable in html    `handsontable`_   same as above
   `pyexcel-pygal`_         svg chart               `pygal`_          2.7, 3.3, 3.4, 3.5
                                                                      3.6, pypy
   `pyexcel-sortable`_      sortable table in html  `csvtotable`_     same as above
   `pyexcel-gantt`_         gantt chart in html     `frappe-gantt`_   except pypy, same
                                                                      as above
   ======================== ======================= ================= ==================

.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text
.. _tabulate: https://bitbucket.org/astanin/python-tabulate
.. _pyexcel-handsontable: https://github.com/pyexcel/pyexcel-handsontable
.. _handsontable: https://cdnjs.com/libraries/handsontable
.. _pyexcel-pygal: https://github.com/pyexcel/pyexcel-chart
.. _pygal: https://github.com/Kozea/pygal
.. _pyexcel-matplotlib: https://github.com/pyexcel/pyexcel-matplotlib
.. _matplotlib: https://matplotlib.org
.. _pyexcel-sortable: https://github.com/pyexcel/pyexcel-sortable
.. _csvtotable: https://github.com/vividvilla/csvtotable
.. _pyexcel-gantt: https://github.com/pyexcel/pyexcel-gantt
.. _frappe-gantt: https://github.com/frappe/gantt

.. rubric:: Footnotes

.. [#f1] zipped csv file
.. [#f2] zipped tsv file


Acknowledgement
===============

All great work have been done by odf, ezodf, xlrd, xlwt, tabulate and other
individual developers. This library unites only the data access code.




License
================================================================================

New BSD License
