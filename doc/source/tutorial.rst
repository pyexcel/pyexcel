Data access
===========

Work with data series in a single sheet
---------------------------------------

Suppose you have the following data in any of the supported excel formats:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

Read an excel file
******************

You can read it use a SeriesReader::

    >> from pyexcel import SeriesReader
    >> reader = SeriesReader("example_series.ods")

Play with data
**************

You can get headers::

    >> print reader.series()
    [u'Column 1', u'Column 2', u'Column 3']

You can use a utility function to get all in a dictionary::

    >> from pyexcel.utils import to_dict
    >> data = to_dict(reader)
    >> print data
    {"Column 2": [4, 5, 6], "Column 3": [7, 8, 9], "Column 1": [1, 2, 3]}

Maybe you want to get only the data without the column headers. You can call ``rows()`` instead::

    >> from pyexcel.utils import to_array
    >> data = to_array(reader.rows())
    >> print data
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

You can get data from the bottom to the top one by calling ``rrows()`` instead::

    >> from pyexcel.utils import to_array
    >> data = to_array(reader.rrows())
    >> print data
    [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

You might want the data arranged vertically. You can call ``columns()`` instead::
	
    >> from pyexcel.utils import to_array
    >> data = to_array(reader.columns())
    >> print data
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

You can get columns in reverse sequence as well by calling ``rcolumns()`` instead::
	
    >> from pyexcel.utils import to_array
    >> data = to_array(reader.columns())
    >> print data
    [[7, 8, 9], [4, 5, 6], [1, 2, 3]]

Do you want to flatten the data? you can get the content in one dimensional array. If you are interested in playing with one dimensional enurmation, you can check out these functions ``enumerate()``, ``reverse()``, ``vertical()``, and ``rvertical()``::

    >> data = to_array(reader.enumerate())
    >> print data
    [1, 4, 7, 2, 5, 8, 3, 6, 9]
    >> data = to_array(reader.reverse())
    >> print data
    [9, 6, 3, 8, 5, 2, 7, 4, 1]
    >> data = to_array(reader.vertical())
    >> print data
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >> data = to_array(reader.rvertical())
    >> print data
    [9, 8, 7, 6, 5, 4, 3, 2, 1]

.. note::

    If you do not want to single column headers out from the data body, you may have a look at the ``Reader`` in the next section


Filter out some data
********************

You may want to filter odd rows and print them in an array of dictionaries::

    >> from pyexcel.filters import OddRowFilter
    >> reader.filter(OddRowFilter())
    >> data = to_array(reader)
    >> print data
    [{u'Column 1': [2]}, {u'Column 2': [5]}, {u'Column 3': [8]}]

Let's try to further filter out even columns::

    >> from pyexcel.filters import EvenColumnFilter
    >> reader.filter(EvenColumnFilter())
    >> data = to_dict(reader)
    >> print data
    {u'Column 3': [8], u'Column 1': [2]}

Save the data
*************

Let's save the previous filtered data::

    >> from pyexcel import Writer
    >> w = Writer("example_series_filter.xls")
    >> w.write_reader(reader)
    >> w.close()

When you open `example_series_filter.xls`, you will find these data:

======== ========
Column 1 Column 3
======== ========
2        8
======== ========


The complete code is::

    from pyexcel import SeriesReader, Writer
    from pyexcel.filters import OddRowFilter
    from pyexcel.filters import EvenColumnFilter

    reader = SeriesReader("example_series.ods")
    reader.filter(OddRowFilter())
    reader.filter(EvenColumnFilter)
    writer = Writer("example_series_filter.xls")
    writer.write_reader(reader)
    writer.close()


Work with pure data in a single sheet file
------------------------------------------

Suppose you have the following data in any of the supported excel formats:

== == == ==
1  2  3  4
5  6  7  8
9  10 11 12
== == == ==

Read an excel file
******************

You can read it use a SeriesReader::

    >> from pyexcel import Reader
    >> reader = Reader("example_series.xls")

Play with data
**************

You can get them in rows or columns::

    >> from pyexcel.utils import to_array
    >> data = to_array(reader.rows())
    >> print data
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    >> from pyexcel.utils import to_array
    >> data = to_array(reader.columns())
    >> print data
    [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

.. note::

   You can explore ``rrows()`` and ``rcolumns()`` too


In the same way, you can get the content in one dimensional array::

    >> data = to_array(reader)
    >> print data
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    >> data = to_array(reader.reverse())
    >> print data
    [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >> data = to_array(reader.vertical())
    >> print data
    [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
    >> data = to_array(reader.rvertical())
    >> print data
    [12,8,4,11,7,3,10,6,2,9,5,1]

And `Reader` has the same filtering capability as `SeriesReader`

Work with multi-sheet file
--------------------------

Read from the workbook
**********************
Suppose you have the following data in any of the supported excel formats.

Sheet 1:

= = =
1 2 3
4 5 6
7 8 9
= = =

Sheet 2:

= = =
X Y Z
1 2 3
4 5 6
= = =

Sheet 3:

= = =
O P Q
3 2 1
4 3 2
= = =

You can easily read them out::

    >> from pyexcel import BookReader
    >> from pyexcel.utils import to_dict
    >> reader = BookReader("example.xls")
    >> my_dict = to_dict(reader)
    >> print my_dict

Per each sheet, you can do custom filtering::

    >> sheet2 = reader[2]
    >> sheet2.add_filter(pyexcel.filters.EvenRowFilter())
	>> my_dict = to_dict(reader)
	>> print my_dict

You will see sheet2 has been applied even row filter::

    {
    u'Sheet 2': [[u'X', u'Y', u'Z'], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], 
    u'Sheet 3': [[u'O', u'P', u'Q'], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]], 
    u'Sheet 1': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
    }

Iterate through each sheet
**************************

Each each sheet is a `Sheet` instance and it accept all filters and iterators you have exercised in previous sections.

You can process sheet by sheet::

    >> from pyexcel.utils import to_array
    >> for sheet in reader: # you may want to do something else
    >>     data = to_array(sheet)
    >>     print data

You may just process Sheet 2 specificially::

    >> sheet = reader["Sheet 2"]
    >> sheet.become_series() # make it aware of column headers
    >> to_dict(sheet) # now regard sheet as an instance of SeriesReader


Write to a work book
********************

Now continue from previous section, you can reverse what it is done in previous section. Write the same dictionary back into a file::

    import pyexcel
    
    
    content = {
        'Sheet 2': 
            [
                ['X', 'Y', 'Z'], 
                [1.0, 2.0, 3.0], 
                [4.0, 5.0, 6.0]
            ], 
        'Sheet 3': 
            [
                ['O', 'P', 'Q'], 
                [3.0, 2.0, 1.0], 
                [4.0, 3.0, 2.0]
            ], 
        'Sheet 1': 
            [
                [1.0, 2.0, 3.0], 
                [4.0, 5.0, 6.0], 
                [7.0, 8.0, 9.0]
            ]
    }
    writer = pyexcel.BookWriter("myfile.ods")
    writer.write_book_from_dict(content)
    writer.close()


How do I read a book, pocess it and save to a new book
******************************************************

Yes, you can do that. The code looks like this::

   from pyexcel import BookReader, BookWriter

   reader = BookReader("yourfile.xls")
   writer = BookWriter("output.xls")
   for sheet in reader:
       new_sheet = writer.create_sheet(sheet.name)
       # do you processing with sheet
       # do filtering? 
       new_sheet.write_from_reader(sheet)
       new_sheet.close()
    writer.close()

What would happen if I save a multi sheet book into "csv" file
**************************************************************

Suppose you have these code::

    import pyexcel
    
    
    content = {
        'Sheet 2': 
            [
                ['X', 'Y', 'Z'], 
                [1.0, 2.0, 3.0], 
                [4.0, 5.0, 6.0]
            ], 
        'Sheet 3': 
            [
                ['O', 'P', 'Q'], 
                [3.0, 2.0, 1.0], 
                [4.0, 3.0, 2.0]
            ], 
        'Sheet 1': 
            [
                [1.0, 2.0, 3.0], 
                [4.0, 5.0, 6.0], 
                [7.0, 8.0, 9.0]
            ]
    }
    writer = pyexcel.BookWriter("myfile.csv")
    writer.write_book_from_dict(content)
    writer.close()

You will end up with three csv files::

    myfile_Sheet 1.csv, myfile_Sheet 2.csv, myfile_Sheet 3.csv

and their content is the value of the dictionary at the corresponding key


Random access to individual cell values in the excel file
---------------------------------------------------------

For single sheet file, you can regard it as two dimensional array if you use `Reader` class. So, you access each cell via this syntax: reader[row][column]. Suppose you have the following data, you can get value 5 by reader[1][1]. And you can refer to row 2 and 3 by reader[1:] or reader[1:3]

= = =
1 2 3
4 5 6
7 8 9
= = =

If you have `SeriesReader`, you can get value 5 by seriesreader[1][1] too because the first row is regarded as column header.

= = =
X Y Z
1 2 3
4 5 6
7 8 9
= = =


For multiple sheet file, you can regard it as three dimensional array if you use `BookReader`. So, you access each cell via this syntax: reader[sheet_index][row][column] or reader["sheet_name"][row][column]. Suppose you have the following sheets. You can get 'P' from sheet 3 by using: bookreader["Sheet 3"][0][1] or bookreader[2][0][1]


Sheet 1:

= = =
1 2 3
4 5 6
7 8 9
= = =

Sheet 2:

= = =
X Y Z
1 2 3
4 5 6
= = =

Sheet 3:

= = =
O P Q
3 2 1
4 3 2
= = =

Data types
===========

Previous section has assumed the data is in the format that you want. In reality, you have to manipulate the data types a bit to suit your needs. Hence, `formatters` comes into the scene. The formatters take effect when the data is read on the fly. They do not affect the persistence of the data in the excel files.

Convert a column of numbers to strings
--------------------------------------

By default, `pyexcel` will render numbers into numbers. For csv file, intergers are read as `int` and float numbers are read as `float`. However, for xls, xlsx and xlsm files, numbers are always read as `float`. Therefore, if you should like to have them in string format, you need to do some conversions. Suppose you have the following data in any of the supported excel formats:

======== =========
userid   name
======== =========
10120    Adam     
10121    Bella
10122    Cedar
======== =========

Let's read it out first::

    >> from pyexcel import SeriesReader
    >> reader = SeriesReader("example.xls")
    >> from pyexcel.utils import to_dict
    >> to_dict(reader)
    {u'userid': [10120.0, 10121.0, 10122.0], u'name': [u'Adam', u'Bella', u'Cedar']}

As you can see, `userid` column is of `float` type. Next, let's convert the column to string format::

    >> from pyexcel.formatters import ColumnFormatter, STRING_FORMAT
    >> formatter = ColumnFormatter(0, STRING_FORMAT)
    >> reader.add_formatter(formatter)
    >> to_dict(reader)
    {u'userid': ['10120.0', '10121.0', '10122.0'], u'name': [u'Adam', u'Bella', u'Cedar']}

Now, they are in string format.

You can do this row by row as well using `RowFormatter` or do this to a whote spread sheet using `SheetFormatter`

Cleanse the cells in a spread sheet
-----------------------------------

Sometimes, the data in a spreadsheet may have unwanted strings in all or some cells. Let's take an example. Suppose we have a spread sheet that contains all strings but it as random spaces before and after the text values. Some field had weird characters, such as "&nbsp;&nbsp;":

================= ============================ ================
        Version        Comments                Author &nbsp;
================= ============================ ================
  v0.0.1          Release versions              &nbsp;Eda
&nbsp; v0.0.2     Useful updates &nbsp; &nbsp;  &nbsp;Freud
================= ============================ ================

First, let's read the content and see what do we have::

    >>> from pyexcel import Reader
    >>> from pyexcel.utils import to_array
    >>> r=Reader("tutorial_datatype_02.ods")
    >>> to_array(r)
    [[u'Version', u'Comments', u'Author &nbsp;'], [u'v0.0.1 ', u'Release versions',
    u'&nbsp;Eda'], [u'&nbsp; V0.02 ', u'Useful updates &nbsp; &nbsp;', u'&nbsp;Freud
    ']]


Now try to create a custom cleanse function::
  
    >>> def cleanse_func(v, t):
    ...     v = v.replace("&nbsp;", "")
    ...     v = v.rstrip().strip()
    ...     return v
    ...

Then let's create a `SheetFormatter` and apply it::

    >>> from pyexcel.formatters import SheetFormatter
    >>> from pyexcel.formatters import STRING_FORMAT
    >>> sf = SheetFormatter(STRING_FORMAT, cleanse_func)
    >>> r.add_formatter(sf)
    >>> to_array(r)
    [[u'Version', u'Comments', u'Author'], [u'v0.0.1', u'Release versions', u'Eda'],
     [u'V0.02', u'Useful updates', u'Freud']]

So in the end, you get this:

================= ============================ ================
        Version        Comments                Author
================= ============================ ================
v0.0.1            Release versions             Eda
v0.0.2            Useful updates               Freud
================= ============================ ================

Excel Sheet Manipulations
=========================

Merge excel books
----------------------

Suppose you have two excel books and each had three sheets. You can merge them and get a new book::

    >>> import pyexcel.BookReader
    >>> merged_book = BookReader("book1.xls") + BookReader("book2.ods")

You also can merge indivdual sheets::

    >>> merged_book = BookReader("book1.xls")["Sheet1"] + BookReader("book2.ods")["Sheet2"]

or::

    >>> merged_book = BookReader("book1.xls")["Sheet1"] + BookReader("book2.ods")

or::

    >>> merged_book = BookReader("book1.xls") + BookReader("book2.ods")["Sheet2"]


Manipulate individual sheets
-----------------------------

merge sheets into a single sheet
*********************************

Suppose you want to merge many csv files row by row into a new sheet.

    >>> import pyexcel
    >>> merged = pyexcel.Reader()
    >>> for file in glob("*.csv"):
    >>>     merged += pyexcel.Reader(file)
    >>> writer = pyexcel.Writer("merged.csv")
    >>> writer.write_reader(merged)
    >>> writer.close()
