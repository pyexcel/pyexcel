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

.. testcode::
   :hide:

   >>> from mock import patch, MagicMock
   >>> import os
   >>> patcher = patch('pyexcel._compact.request.urlopen')
   >>> fake_url_open = patcher.start()
   >>> response = MagicMock()
   >>> response.type.return_value = 'application/vnd.ms-excel'
   >>> method = MagicMock()
   >>> xls_file = open(os.path.join("examples", "basics", "multiple-sheets-example.xls"), 'rb')
   >>> method.info.return_value = response
   >>> method.read.return_value = xls_file.read()
   >>> fake_url_open.return_value = method
   >>> xls_file.close()

.. code-block::

   >>> another_sheet.url = "https://github.com/pyexcel/pyexcel/raw/master/examples/basics/multiple-sheets-example.xls"
   >>> another_sheet.content
   +---+---+---+
   | 1 | 2 | 3 |
   +---+---+---+
   | 4 | 5 | 6 |
   +---+---+---+
   | 7 | 8 | 9 |
   +---+---+---+

.. testcode::
   :hide:

   >>> patcher.stop()
