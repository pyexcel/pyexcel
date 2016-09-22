Dot notation for data source
================================================================================

Since version 0.3.0, the data source becomes an attribute of the pyexcel native
classes. All support data format is a dot notation away.

.. code-block:: python

    >>> import pyexcel
    >>> content = "1,2,3\n3,4,5"
    >>> sheet = pyexcel.get_sheet(file_type="csv", file_content=content)
    >>> sheet.tsv
    '1\t2\t3\r\n3\t4\t5\r\n'
    >>> sheet.xls # doctest: +ELLIPSIS
    '...
    >>> sheet.ods # doctest: +ELLIPSIS
    '...
    >>> print sheet.simple
    csv:
    -  -  -
    1  2  3
    3  4  5
    -  -  -

What's more, you could as well set value to an attribute, for example:

.. code-block:: python

    >>> import pyexcel
    >>> content = "1,2,3\n3,4,5"
    >>> sheet = pyexcel.Sheet()
    >>> sheet.csv = content
    >>> sheet.array
    [[1, 2, 3], [3, 4, 5]]

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

It can used when you want to get a :class:`pyexcel.Sheet` out from an incoming
data stream, e.g. from http protocol, or from a zip archive.


