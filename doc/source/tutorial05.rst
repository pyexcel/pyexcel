Data manipulation in a sheet
============================

Update one column of a data file
---------------------------------

Suppose have one data file as the following:

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

    from pyexcel import SeriesReader, Writer


	reader = SeriesReader("example1.csv")
    reader.set_named_column_at("Column 2", [11, 12, 13])
	writer = Writer("output.xls")
	writer.write_reader(reader)

Your output.xls will have these data:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        11       7
2        12       8
3        13       9
======== ======== ========
