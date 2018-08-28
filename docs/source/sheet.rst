Sheet
==========

Random access
-----------------

To randomly access a cell of :class:`~pyexcel.Sheet` instance, two
syntax are available::

    sheet[row, column]

or::

    sheet['A1']

The former syntax is handy when you know the row and column numbers.
The latter syntax is introduced to help you convert the excel column header
such as "AX" to integer numbers.

Suppose you have the following data, you can get value 5 by reader[2, 2].

.. pyexcel-table::

   ---pyexcel:example data---
   Example,X,Y,Z
   a,1,2,3
   b,4,5,6
   c,7,8,9


Here is the example code showing how you can randomly access a cell:

.. testcode::
   :hide:

   >>> import pyexcel
   >>> data = [
   ...     ['Example', 'X', 'Y', 'Z'],
   ...     ['a', 1, 2, 3],
   ...     ['b', 4, 5, 6],
   ...     ['c', 7, 8, 9]]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

.. testcode::

   >>> sheet = pyexcel.get_sheet(file_name="example.xls")
   >>> sheet.content
   +---------+---+---+---+
   | Example | X | Y | Z |
   +---------+---+---+---+
   | a       | 1 | 2 | 3 |
   +---------+---+---+---+
   | b       | 4 | 5 | 6 |
   +---------+---+---+---+
   | c       | 7 | 8 | 9 |
   +---------+---+---+---+
   >>> print(sheet[2, 2])
   5
   >>> print(sheet["C3"])
   5
   >>> sheet[3, 3] = 10
   >>> print(sheet[3, 3])
   10


.. note::

   In order to set a value to a cell, please use
   sheet[row_index, column_index] = new_value


**Random access to rows and columns**

.. testcode::
   :hide:

   >>> sheet[1, 0] = str(sheet[1, 0])
   >>> str(sheet[1,0])
   'a'
   >>> sheet[0, 2] = str(sheet[0, 2])
   >>> sheet[0, 2]
   'Y'

Continue with previous excel file, you can access
row and column separately::

    >>> sheet.row[1]
    ['a', 1, 2, 3]
    >>> sheet.column[2]
    ['Y', 2, 5, 8]


**Use custom names instead of index**
Alternatively, it is possible to use the first row to
refer to each columns::

    >>> sheet.name_columns_by_row(0)
    >>> print(sheet[1, "Y"])
    5
    >>> sheet[1, "Y"] = 100
    >>> print(sheet[1, "Y"])
    100

You have noticed the row index has been changed. It is because
first row is taken as the column names, hence all rows after
the first row are shifted. Now accessing the columns are
changed too::

    >>> sheet.column['Y']
    [2, 100, 8]

Hence access the same cell, this statement also works::

    >>> sheet.column['Y'][1]
    100

Further more, it is possible to use first column to refer to each rows::

    >>> sheet.name_rows_by_column(0)

To access the same cell, we can use this line::

    >>> sheet.row["b"][1]
    100

For the same reason, the row index has been reduced by 1. Since we
have named columns and rows, it is possible to access the same cell
like this::

    >>> print(sheet["b", "Y"])
    100
    >>> sheet["b", "Y"] = 200
    >>> print(sheet["b", "Y"])
    200


**Play with data**

Suppose you have the following data in any of the supported
excel formats again:

.. pyexcel-table::

   ---pyexcel:data with columns---
   Column 1,Column 2,Column 3
   1,4,7
   2,5,8
   3,6,9


.. testcode::
   :hide:

   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 2, 3],
   ...      [4, 5, 6],
   ...      [7, 8, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example_series.xls")

.. testcode::

   >>> sheet = pyexcel.get_sheet(file_name="example_series.xls",
   ...      name_columns_by_row=0)

.. testcode::
   :hide:

   >>> sheet.colnames = [ str(name) for name in sheet.colnames]

You can get headers::

    >>> print(list(sheet.colnames))
    ['Column 1', 'Column 2', 'Column 3']

You can use a utility function to get all in a dictionary::

    >>> sheet.to_dict()
    OrderedDict([('Column 1', [1, 4, 7]), ('Column 2', [2, 5, 8]), ('Column 3', [3, 6, 9])])

Maybe you want to get only the data without the column headers.
You can call :meth:`~pyexcel.Sheet.rows()` instead::

    >>> list(sheet.rows())
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

You can get data from the bottom to the top one by
 calling :meth:`~pyexcel.Sheet.rrows()`::

    >>> list(sheet.rrows())
    [[7, 8, 9], [4, 5, 6], [1, 2, 3]]

You might want the data arranged vertically. You can call
:meth:`~pyexcel.Sheet.columns()`::

    >>> list(sheet.columns())
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

You can get columns in reverse sequence as well by calling
:meth:`~pyexcel.Sheet.rcolumns()`::

    >>> list(sheet.rcolumns())
    [[3, 6, 9], [2, 5, 8], [1, 4, 7]]

Do you want to flatten the data? You can get the content in one
dimensional array. If you are interested in playing with one
dimensional enumeration, you can check out these functions
:meth:`~pyexcel.Sheet.enumerate`, :meth:`~pyexcel.Sheet.reverse`,
:meth:`~pyexcel.Sheet.vertical`, and :meth:`~pyexcel.Sheet.rvertical()`::

    >>> list(sheet.enumerate())
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> list(sheet.reverse())
    [9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> list(sheet.vertical())
    [1, 4, 7, 2, 5, 8, 3, 6, 9]
    >>> list(sheet.rvertical())
    [9, 6, 3, 8, 5, 2, 7, 4, 1]


**attributes**

Attributes::

    >>> import pyexcel
    >>> content = "1,2,3\n3,4,5"
    >>> sheet = pyexcel.get_sheet(file_type="csv", file_content=content)
    >>> sheet.tsv
    '1\t2\t3\r\n3\t4\t5\r\n'
    >>> print(sheet.simple)
    csv:
    -  -  -
    1  2  3
    3  4  5
    -  -  -

What's more, you could as well set value to an attribute, for example::
    >>> import pyexcel
    >>> content = "1,2,3\n3,4,5"
    >>> sheet = pyexcel.Sheet()
    >>> sheet.csv = content
    >>> sheet.array
    [[1, 2, 3], [3, 4, 5]]

You can get the direct access to underneath stream object. In some situation,
it is desired::

    >>> stream = sheet.stream.tsv

The returned stream object has tsv formatted content for reading.


What you could further do is to set a memory stream of any supported file format
to a sheet. For example:

    >>> another_sheet = pyexcel.Sheet()
    >>> another_sheet.xls = sheet.xls
    >>> another_sheet.content
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 3 | 4 | 5 |
    +---+---+---+

Yet, it is possible assign a absolute url to an online excel file
to an instance of :class:`pyexcel.Sheet`.

**custom attributes**

You can pass on source specific parameters to getter and setter functions.

.. code-block:: python

    >>> content = "1-2-3\n3-4-5"
    >>> sheet = pyexcel.Sheet()
    >>> sheet.set_csv(content, delimiter="-")
    >>> sheet.csv
    '1,2,3\r\n3,4,5\r\n'
    >>> sheet.get_csv(delimiter="|")
    '1|2|3\r\n3|4|5\r\n'



Data manipulation 
--------------------------------------------------------------------------------

The data in a sheet is represented by :class:`~pyexcel.Sheet` which maintains the data
as a list of lists. You can regard :class:`~pyexcel.Sheet` as a two dimensional array
with additional iterators. Random access to individual column and row is exposed
by :class:`~pyexcel.sheets.column.Column` and :class:`~pyexcel.sheets.row.Row` 


Column manipulation
********************************************************************************

.. testcode::
   :hide:

   >>> import pyexcel
   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 4, 7],
   ...      [2, 5, 8],
   ...      [3, 6, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example.xls")

Suppose have one data file as the following:

.. code-block:: python

    >>> sheet = pyexcel.get_sheet(file_name="example.xls", name_columns_by_row=0)
    >>> sheet
    pyexcel sheet:
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 1        | 4        | 7        |
    +----------+----------+----------+
    | 2        | 5        | 8        |
    +----------+----------+----------+
    | 3        | 6        | 9        |
    +----------+----------+----------+

And you want to update ``Column 2`` with these data: [11, 12, 13]

.. code-block:: python

    >>> sheet.column["Column 2"] = [11, 12, 13]
    >>> sheet.column[1]
    [11, 12, 13]
    >>> sheet
    pyexcel sheet:
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 1        | 11       | 7        |
    +----------+----------+----------+
    | 2        | 12       | 8        |
    +----------+----------+----------+
    | 3        | 13       | 9        |
    +----------+----------+----------+

Remove one column of a data file
*********************************

If you want to remove ``Column 2``, you can just call:

.. code-block:: python

    >>> del sheet.column["Column 2"]
    >>> sheet.column["Column 3"]
    [7, 8, 9]

The sheet content will become:

.. code-block:: python

    >>> sheet
    pyexcel sheet:
    +----------+----------+
    | Column 1 | Column 3 |
    +==========+==========+
    | 1        | 7        |
    +----------+----------+
    | 2        | 8        |
    +----------+----------+
    | 3        | 9        |
    +----------+----------+


Append more columns to a data file
********************************************************************************

Continue from previous example. Suppose you want add two more
columns to the data file

======== ========
Column 4 Column 5
======== ========
10       13
11       14
12       15
======== ========

Here is the example code to append two extra columns:

.. code-block:: python

   >>> extra_data = [
   ...    ["Column 4", "Column 5"],
   ...    [10, 13],
   ...    [11, 14],
   ...    [12, 15]
   ... ]
   >>> sheet2 = pyexcel.Sheet(extra_data)
   >>> sheet.column += sheet2
   >>> sheet.column["Column 4"]
   [10, 11, 12]
   >>> sheet.column["Column 5"]
   [13, 14, 15]

Here is what you will get:

.. code-block:: python

    >>> sheet
    pyexcel sheet:
    +----------+----------+----------+----------+
    | Column 1 | Column 3 | Column 4 | Column 5 |
    +==========+==========+==========+==========+
    | 1        | 7        | 10       | 13       |
    +----------+----------+----------+----------+
    | 2        | 8        | 11       | 14       |
    +----------+----------+----------+----------+
    | 3        | 9        | 12       | 15       |
    +----------+----------+----------+----------+


Cherry pick some columns to be removed
***************************************

Suppose you have the following data:

.. code-block:: python

     >>> data = [
     ...     ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
     ...     [1,2,3,4,5,6,7,9],
     ... ]
     >>> sheet = pyexcel.Sheet(data, name_columns_by_row=0)
     >>> sheet
     pyexcel sheet:
     +---+---+---+---+---+---+---+---+
     | a | b | c | d | e | f | g | h |
     +===+===+===+===+===+===+===+===+
     | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
     +---+---+---+---+---+---+---+---+

And you want to remove columns named as: 'a', 'c, 'e', 'h'. This is how you do it:

.. code-block:: python

     >>> del sheet.column['a', 'c', 'e', 'h']
     >>> sheet
     pyexcel sheet:
     +---+---+---+---+
     | b | d | f | g |
     +===+===+===+===+
     | 2 | 4 | 6 | 7 |
     +---+---+---+---+

What if the headers are in a different row
********************************************************************************

.. testcode::
   :hide:

   >>> data = [
   ...     [1, 2, 3],
   ...     ["Column 1", "Column 2", "Column 3"],
   ...     [4, 5, 6]
   ... ]
   >>> sheet = pyexcel.Sheet(data)

Suppose you have the following data:

.. code-block:: python

   >>> sheet
   pyexcel sheet:
   +----------+----------+----------+
   | 1        | 2        | 3        |
   +----------+----------+----------+
   | Column 1 | Column 2 | Column 3 |
   +----------+----------+----------+
   | 4        | 5        | 6        |
   +----------+----------+----------+

The way to name your columns is to use index 1:

.. code-block:: python

   >>> sheet.name_columns_by_row(1)

Here is what you get:

.. code-block:: python

   >>> sheet
   pyexcel sheet:
   +----------+----------+----------+
   | Column 1 | Column 2 | Column 3 |
   +==========+==========+==========+
   | 1        | 2        | 3        |
   +----------+----------+----------+
   | 4        | 5        | 6        |
   +----------+----------+----------+


Row manipulation
********************************************************************************

.. testcode::
   :hide:

   >>> data = [
   ...     ["a", "b", "c", "Row 1"],
   ...     ["e", "f", "g", "Row 2"],
   ...     [1, 2, 3, "Row 3"]
   ... ]
   >>> sheet = pyexcel.Sheet(data)

Suppose you have the following data:

.. code-block:: python

   >>> sheet
   pyexcel sheet:
   +---+---+---+-------+
   | a | b | c | Row 1 |
   +---+---+---+-------+
   | e | f | g | Row 2 |
   +---+---+---+-------+
   | 1 | 2 | 3 | Row 3 |
   +---+---+---+-------+

You can name your rows by column index at 3:

.. code-block:: python

    >>> sheet.name_rows_by_column(3)
    >>> sheet
    pyexcel sheet:
    +-------+---+---+---+
    | Row 1 | a | b | c |
    +-------+---+---+---+
    | Row 2 | e | f | g |
    +-------+---+---+---+
    | Row 3 | 1 | 2 | 3 |
    +-------+---+---+---+

Then you can access rows by its name:

.. code-block:: python

   >>> sheet.row["Row 1"]
   ['a', 'b', 'c']

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example.xls")


Formatting
--------------------------------------------------------------------------------


Previous section has assumed the data is in the format that you want. In reality, you have to
manipulate the data types a bit to suit your needs. Hence, formatters comes into the scene.
use :meth:`~pyexcel.Sheet.format` to apply formatter immediately. 

.. note::

   **int**, **float** and **datetime** values are automatically detected in **csv** files
   since **pyexcel** version 0.2.2


Convert a column of numbers to strings
********************************************************************************

Suppose you have the following data:

.. code-block:: python

   >>> import pyexcel
   >>> data = [
   ...     ["userid","name"],
   ...     [10120,"Adam"],  
   ...     [10121,"Bella"],
   ...     [10122,"Cedar"]
   ... ]
   >>> sheet = pyexcel.Sheet(data)
   >>> sheet.name_columns_by_row(0)
   >>> sheet.column["userid"]
   [10120, 10121, 10122]

As you can see, `userid` column is of `int` type. Next, let's convert the column to string format:

.. code-block:: python

    >>> sheet.column.format("userid", str)
    >>> sheet.column["userid"]
    ['10120', '10121', '10122']

.. _cleansing:

Cleanse the cells in a spread sheet
********************************************************************************

Sometimes, the data in a spreadsheet may have unwanted strings in all or some
cells. Let's take an example. Suppose we have a spread sheet that contains
all strings but it as random spaces before and after the text values. Some
field had weird characters, such as "&nbsp;&nbsp;":

.. code-block:: python

   >>> data = [
   ...     ["        Version", "        Comments", "       Author &nbsp;"],
   ...     ["  v0.0.1       ", " Release versions","           &nbsp;Eda"],
   ...     ["&nbsp; v0.0.2  ", "Useful updates &nbsp; &nbsp;", "  &nbsp;Freud"]
   ... ]
   >>> sheet = pyexcel.Sheet(data)
   >>> sheet.content
   +-----------------+------------------------------+----------------------+
   |         Version |         Comments             |        Author &nbsp; |
   +-----------------+------------------------------+----------------------+
   |   v0.0.1        |  Release versions            |            &nbsp;Eda |
   +-----------------+------------------------------+----------------------+
   | &nbsp; v0.0.2   | Useful updates &nbsp; &nbsp; |   &nbsp;Freud        |
   +-----------------+------------------------------+----------------------+


Now try to create a custom cleanse function::
  
.. code-block:: python

    >>> def cleanse_func(v):
    ...     v = v.replace("&nbsp;", "")
    ...     v = v.rstrip().strip()
    ...     return v
    ...

Then let's create a :class:`~pyexcel.SheetFormatter` and apply it::

.. code-block:: python

    >>> sheet.map(cleanse_func)

So in the end, you get this:

.. code-block:: python

    >>> sheet.content
    +---------+------------------+--------+
    | Version | Comments         | Author |
    +---------+------------------+--------+
    | v0.0.1  | Release versions | Eda    |
    +---------+------------------+--------+
    | v0.0.2  | Useful updates   | Freud  |
    +---------+------------------+--------+


Data filtering
--------------------------------------------------------------------------------

use :meth:`~pyexcel.Sheet.filter` function to apply a filter immediately. The content is modified.


Suppose you have the following data in any of the supported excel formats:

======== ======== ========
Column 1 Column 2 Column 3
======== ======== ========
1        4        7
2        5        8
3        6        9
======== ======== ========

    >>> import pyexcel

.. testcode::
   :hide:

   >>> import os
   >>> data = [
   ...      ["Column 1", "Column 2", "Column 3"],
   ...      [1, 2, 3],
   ...      [4, 5, 6],
   ...      [7, 8, 9]
   ...  ]
   >>> s = pyexcel.Sheet(data)
   >>> s.save_as("example_series.xls")

.. code-block:: python

    >>> sheet = pyexcel.get_sheet(file_name="example_series.xls", name_columns_by_row=0)
    >>> sheet.content
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 1        | 2        | 3        |
    +----------+----------+----------+
    | 4        | 5        | 6        |
    +----------+----------+----------+
    | 7        | 8        | 9        |
    +----------+----------+----------+

Filter out some data
********************************************************************************

You may want to filter odd rows and print them in an array of dictionaries:

.. code-block:: python

    >>> sheet.filter(row_indices=[0, 2])
    >>> sheet.content
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +==========+==========+==========+
    | 4        | 5        | 6        |
    +----------+----------+----------+

Let's try to further filter out even columns:

.. code-block:: python

    >>> sheet.filter(column_indices=[1])
    >>> sheet.content
    +----------+----------+
    | Column 1 | Column 3 |
    +==========+==========+
    | 4        | 6        |
    +----------+----------+

Save the data
*************

Let's save the previous filtered data:

.. code-block:: python

    >>> sheet.save_as("example_series_filter.xls")

When you open `example_series_filter.xls`, you will find these data

======== ========
Column 1 Column 3
======== ========
2        8
======== ========

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example_series_filter.xls")


How to filter out empty rows in my sheet?
**************************************************

Suppose you have the following data in a sheet and you want to remove those rows with blanks:

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.Sheet([[1,2,3],['','',''],['','',''],[1,2,3]])

You can use :class:`pyexcel.filters.RowValueFilter`, which examines each row, return `True` if the row should be filtered out. So, let's define a filter function:

.. code-block:: python

    >>> def filter_row(row_index, row):
    ...     result = [element for element in row if element != '']
    ...     return len(result)==0


And then apply the filter on the sheet:

.. code-block:: python

    >>> del sheet.row[filter_row]
    >>> sheet
    pyexcel sheet:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+

   

.. testcode::
   :hide:

   >>> os.unlink("example_series.xls")
