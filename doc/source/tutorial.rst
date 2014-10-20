Simple usage
=============

Random access to individual cell values in the excel file
---------------------------------------------------------

For single sheet file, you can regard it as two dimensional array if you use `Reader` class. So, you access each cell via this syntax: reader[row][column]. Suppose you have the following data, you can get value 5 by reader[1][1]. And you can refer to row 2 and 3 by reader[1:] or reader[1:3]

= = =
1 2 3
4 5 6
7 8 9
= = =

Here is the example code showing how you can randomly access a cell::

    >>> import pyexcel
    >>> reader = pyexcel.Reader("example.csv""")
    >>> print reader[1][1]
    5

If you have `SeriesReader`, you can get value 5 by seriesreader[1][1] too because the first row is regarded as column header.

= = =
X Y Z
1 2 3
4 5 6
7 8 9
= = =

Here is the example code showing how you can randomly access a cell::

    >>> import pyexcel
    >>> reader = pyexcel.SeriesReader("example.csv""")
    >>> print reader[1][1]
    5

For multiple sheet file, you can regard it as three dimensional array if you use `Book`. So, you access each cell via this syntax: reader[sheet_index][row][column] or reader["sheet_name"][row][column]. Suppose you have the following sheets. You can get 'P' from sheet 3 by using: bookreader["Sheet 3"][0][1] or bookreader[2][0][1]


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

And you can randomly access a cell in a sheet::

    >>> import pyexcel
    >>> reader = pyexcel.Book("example.xls")
    >>> print(reader[0][0][0])
    1
    >>> print(reader["Sheet 1"][0][0])
    1

.. TIP::
  With pyexcel, you can regard single sheet reader as an two dimensional array and multi-sheet excel book reader as a ordered dictionary of two dimensional arrays.

Reading a single sheet excel file
---------------------------------
Suppose you have a csv, xls, xlsx file as the following:

= = =
1 2 3
4 5 6
7 8 9
= = =

The following code will give you the data in json::

    from pyexcel import Reader
    from pyexcel.utils import to_array
    import json
    
    # "example.xls","example.xlsx","example.xlsm"
    reader = Reader("example.csv")
    data = to_array(reader)
    print json.dumps(data)


The output is::

    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

Read the sheet as a dictionary
******************************
Suppose you have a csv, xls, xlsx file as the following:

======== ========= ========
Column 1 Column 2  Column 3
======== ========= ========
1        4         7
2        5         8
3        6         9
======== ========= ========

The following code will give you data series in a dictionary:

.. code-block:: python

    from pyexcel import SeriesReader
    from pyexcel.utils import to_dict
    
    # "example.xls","example.xlsx","example.xlsm"
    reader = SeriesReader("example.csv")
    data = to_dict(reader)
    print data


The output is::

    {"Column 1": [1, 2, 3], "Column 2": [4, 5, 6], "Column 3": [7, 8, 9]}

Can I get an array of dictionaries per each row?
*************************************************

Returning to previous example:

= = =
X Y Z
1 2 3
4 5 6
7 8 9
= = =

The following code will produce what you want::

    from pyexcel import SeriesReader
    from pyexcel.utils import to_records
    import json
    
    # "example.xls","example.xlsx","example.xlsm"
    reader = SeriesReader("example.csv")
    data = to_record(reader)
    print json.dumps(data)


The output is::

    [{"X":1, "Y":2, "Z":3}, {"X":4 ...}, ... ]


Writing a single sheet excel file
---------------------------------

Suppose you have an array as the following:

= = =
1 2 3
4 5 6
7 8 9
= = =

The following code will write it as an excel file of your choice::


    from pyexcel import Writer
    
    array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # "output.xls" "output.xlsx" "output.ods" "output.xlsm"
    writer = Writer("output.csv")
    writer.write_array(array)
    writer.close()


Suppose you have a dictionary as the following:

======== ========= ========
Column 1 Column 2  Column 3
======== ========= ========
1        4         7
2        5         8
3        6         9
======== ========= ========

The following code will write it as an excel file of your choice::

    from pyexcel import Writer
    
    example_dict = {"Column 1": [1, 2, 3], "Column 2": [4, 5, 6], "Column 3": [7, 8, 9]}
    # "output.xls" "output.xlsx" "output.ods" "output.xlsm"
    writer = Writer("output.csv")
    writer.write_dict(example_dict)
    writer.close()


Read multiple sheet excel file
------------------------------

Suppose you have a book like this:

= = =
1 2 3
4 5 6
7 8 9
= = =

Sheet 1

= = =
X Y Z
1 2 3
4 5 6
= = =

Sheet 2

= = =
O P Q
3 2 1
4 3 2
= = =

Sheet 3

You can get a dictionary out of it by the following code::

    import pyexcel
    
    
    reader = pyexcel.Reader("example.xls")
    my_dict = pyexcel.utils.to_dict(reader)
    print(my_dict)

the output is::

    {
    u'Sheet 1': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
    u'Sheet 2': [[u'X', u'Y', u'Z'], [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], 
    u'Sheet 3': [[u'O', u'P', u'Q'], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]]
    }


Write multiple sheet excel file
-------------------------------

Suppose you have previous data as a dictionary and you want to save it as multiple sheet excel file::

    import pyexcel
    
    
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
    writer = pyexcel.BookWriter("myfile.xls")
    writer.write_book_from_dict(content)
    writer.close()

You shall get a xls file 
