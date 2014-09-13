Simple usage
=============

Update one column of a data file
---------------------------------

Suppose you want to merge the following two data files:

example1.csv

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

And you want to update ``Column 2`` with these data: [11, 12, 13]

Here is the code::

    from pyexcel.processings import update_a_column

    
    custom_column = {"Column 2":[11, 12, 13]}
    update_a_column("example1.csv", custom_column, "output.xls")

Your oupt.xls will have these data:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        11       7
2        12       8
3        13       9
======== ======== ========


Merge two files into one
-------------------------

Suppose you want to merge the following two data files:

example1.csv

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

example2.ods

======== ========
Column 4 Column 5
======== ========
10       12      
11       13      
======== ========

The following code will merge the tow into one file, say "output.xls"::

    from pyexcel.processings import merge_two_files


    merge_two_files("example1.csv", "example2.ods", "output.xls")

The output.xls would have the following data:

======== ======== ======== ======== ========
Column 1 Column 2 Column 3 Column 4 Column 5
======== ======== ======== ======== ========
1        4        7        10       12      
2        5        8        11       13      
3        6        9
======== ======== ======== ======== ========


Select candidate columns of two files and form a new one
--------------------------------------------------------

Suppose you have these two files:

example.ods

======== ======== ======== ======== ========
Column 1 Column 2 Column 3 Column 4 Column 5
======== ======== ======== ======== ========
1        4        7        10       13      
2        5        8        11       14      
3        6        9        12       15
======== ======== ======== ======== ========

example.xls

======== ======== ======== ======== =========
Column 6 Column 7 Column 8 Column 9 Column 10
======== ======== ======== ======== =========
16       17       18       19       20
======== ======== ======== ======== =========

And you want to filter out column 2 and 4 from example.ods,  filter out column 6 and 7 and merge them:

======== ======== ======== ======== ======== =========
Column 1 Column 3 Column 5 Column 8 Column 9 Column 10
======== ======== ======== ======== ======== =========
1        7        13       18       19       20		 
2        8        14                                    
3        9        15                           
======== ======== ======== ======== ======== =========

The following code will do the job::

    from pyexcel.processings import merge_two_readers
    from pyexcel import SeriesReader
    from pyexcel.filters import EvenColumnFilter, ColumnFilter


    reader1 = pyexcel.SeriesReader("example.ods")
    reader2 = pyexcel.SeriesReader("example.xls")
    reader1.filter(EvenColumnFilter())
    reader2.filter(ColumnFilter([6,7]))
    merge_two_readers(reader1, reader2, "output.xls")
 
