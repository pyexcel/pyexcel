.. _formatting:

Sheet: Formatting
===================

Previous section has assumed the data is in the format that you want. In reality, you have to
manipulate the data types a bit to suit your needs. Hence, formatters comes into the scene.
use :meth:`~pyexcel.Sheet.format` to apply formatter immediately. 

.. note::

   **int**, **float** andate **datetime** values are automatically detected in **csv** files
   since **pyexcel** version 0.2.2


Convert a column of numbers to strings
--------------------------------------

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
-----------------------------------

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
