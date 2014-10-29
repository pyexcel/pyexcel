Filtering cells
================

There are three ways of applying a filter:

#. use `add_filter`, `remove_filter` and `clear_filter` to interactively apply a filter. The content is not modified until you call `freeze_filters`
#. use `filter` function to apply a filter immediately. The content is modified.

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

    >> import pyexcel as pe
    >> reader = pe.SeriesReader("example_series.ods")

Play with data
**************

You can get headers::

    >> print reader.series()
    [u'Column 1', u'Column 2', u'Column 3']

You can use a utility function to get all in a dictionary::

    >> data = pe.to_dict(reader)
    >> print data
    { "Column 1": [1, 2, 3], "Column 2": [4, 5, 6], "Column 3": [7, 8, 9]}

Maybe you want to get only the data without the column headers. You can call ``rows()`` instead::

    >> data = pe.to_array(reader.rows())
    >> print data
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

You can get data from the bottom to the top one by calling ``rrows()`` instead::

    >> data = pe.to_array(reader.rrows())
    >> print data
    [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

You might want the data arranged vertically. You can call ``columns()`` instead::
	
    >> data = pe.to_array(reader.columns())
    >> print data
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

You can get columns in reverse sequence as well by calling ``rcolumns()`` instead::
	
    >> data = pe.to_array(reader.columns())
    >> print data
    [[7, 8, 9], [4, 5, 6], [1, 2, 3]]

Do you want to flatten the data? you can get the content in one dimensional array. If you are interested in playing with one dimensional enurmation, you can check out these functions ``enumerate()``, ``reverse()``, ``vertical()``, and ``rvertical()``::

    >> data = pe.to_array(reader.enumerate())
    >> print data
    [1, 4, 7, 2, 5, 8, 3, 6, 9]
    >> data = pe.to_array(reader.reverse())
    >> print data
    [9, 6, 3, 8, 5, 2, 7, 4, 1]
    >> data = pe.to_array(reader.vertical())
    >> print data
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >> data = pe.to_array(reader.rvertical())
    >> print data
    [9, 8, 7, 6, 5, 4, 3, 2, 1]

.. note::

    If you do not want to single column headers out from the data body, you may have a look at the ``Reader`` in the next section


Filter out some data
********************

You may want to filter odd rows and print them in an array of dictionaries::

    >> reader.filter(pe.filters.OddRowFilter())
    >> data = pe.to_array(reader)
    >> print data
    [{u'Column 1': [2]}, {u'Column 2': [5]}, {u'Column 3': [8]}]

Let's try to further filter out even columns::

    >> reader.filter(pe.filters.EvenColumnFilter())
    >> data = pe.to_dict(reader)
    >> print data
    {u'Column 3': [8], u'Column 1': [2]}

Save the data
*************

Let's save the previous filtered data::

    >> import pyexcel as pe
    >> w = pe.Writer("example_series_filter.xls")
    >> w.write_reader(reader)
    >> w.close()

When you open `example_series_filter.xls`, you will find these data:

======== ========
Column 1 Column 3
======== ========
2        8
======== ========


The complete code is::

    import pyexcel as pe

    reader = pe.SeriesReader("example_series.ods")
    reader.filter(pe.filters.OddRowFilter())
    reader.filter(pe.filters.EvenColumnFilter)
    writer = pe.Writer("example_series_filter.xls")
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

    >> import pyexcel as pe
    >> reader = pe.Reader("example_series.xls")

Play with data
**************

You can get them in rows or columns::

    >> data = pe.to_array(reader.rows())
    >> print data
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    >> data = pe.to_array(reader.columns())
    >> print data
    [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

.. note::

   You can explore ``rrows()`` and ``rcolumns()`` too


In the same way, you can get the content in one dimensional array::

    >> data = pe.to_array(reader)
    >> print data
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    >> data = pe.to_array(reader.reverse())
    >> print data
    [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >> data = pe.to_array(reader.vertical())
    >> print data
    [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
    >> data = pe.to_array(reader.rvertical())
    >> print data
    [12,8,4,11,7,3,10,6,2,9,5,1]

And `Reader` has the same filtering capability as `SeriesReader`

Work with multi-sheet file
--------------------------

Read from the workbook
**********************

Previous section explained already how to read from a work book. This section stresses that per each sheet, you can do custom filtering::

    >> sheet2 = reader[2]
    >> sheet2.add_filter(pyexcel.filters.EvenRowFilter())
    >> my_dict = pe.to_dict(reader)
    >> print my_dict

You will see sheet2 has been applied even row filter::

    {
    u'Sheet 1': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
    u'Sheet 2': [[u'X', u'Y', u'Z'], [4.0, 5.0, 6.0]], 
    u'Sheet 3': [[u'O', u'P', u'Q'], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]]
    }

Iterate through each sheet
**************************

Each each sheet is a `Sheet` instance and it accept all filters and iterators you have exercised in previous sections.

You can process sheet by sheet::

    for sheet in reader: # you may want to do something else
         data = pe.to_array(sheet)
         print data

You may just process Sheet 2 specificially::

    >> sheet = reader["Sheet 2"]
    >> sheet.become_series() # make it aware of column headers
    >> pe.to_dict(sheet) # now regard sheet as an instance of SeriesReader


Write to a work book
********************

You can write a dictionary back to any file formats as you read the `Simple Usage` section. Keys will become the sheet names and values become the data content.

How do I read a book, pocess it and save to a new book
******************************************************

Yes, you can do that. The code looks like this::

   import pyexcel as pe

   reader = pe.Book("yourfile.xls")
   writer = pe.BookWriter("output.xls")
   for sheet in reader:
       new_sheet = writer.create_sheet(sheet.name)
       # do you processing with sheet
       # do filtering? 
       new_sheet.write_from_reader(sheet)
       new_sheet.close()
    writer.close()

What would happen if I save a multi sheet book into "csv" file
**************************************************************

Well, you will get one csv file per each sheet. Suppose you have these code::

    import pyexcel as pe
    
    
    content = {
        'Sheet 1': 
            [
                [1.0, 2.0, 3.0], 
                [4.0, 5.0, 6.0], 
                [7.0, 8.0, 9.0]
            ],
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
            ] 
    }
    writer = pe.BookWriter("myfile.csv")
    writer.write_book_from_dict(content)
    writer.close()

You will end up with three csv files::

    myfile_Sheet 1.csv, myfile_Sheet 2.csv, myfile_Sheet 3.csv

and their content is the value of the dictionary at the corresponding key

