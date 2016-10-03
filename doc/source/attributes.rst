Dot notation for data source
================================================================================

Since version 0.3.0, the data source becomes an attribute of the pyexcel native
classes. All support data format is a dot notation away.


For sheet
--------------------------------------------------------------------------------

Get content
************

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
    >>> print(sheet.simple)
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

Set content
************

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

Yet, it is possible assign a absolute url to an online excel file to an instance of
 :class:`pyexcel.Sheet`.

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

.. code-block:: python

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

   
For book
--------------------------------------------------------------------------------

The same dot notation is avaiable to :class:`pyexcel.Book` as well.

Get content
************

.. code-block:: python

    >>> book_dict = {
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
    ...          ],
    ...      'Sheet 1':
    ...          [
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0],
    ...              [7.0, 8.0, 9.0]
    ...          ]
    ...  }
    >>> book = pyexcel.get_book(bookdict=book_dict)
    >>> book
    Sheet 1:
    +-----+-----+-----+
    | 1.0 | 2.0 | 3.0 |
    +-----+-----+-----+
    | 4.0 | 5.0 | 6.0 |
    +-----+-----+-----+
    | 7.0 | 8.0 | 9.0 |
    +-----+-----+-----+
    Sheet 2:
    +-----+-----+-----+
    | X   | Y   | Z   |
    +-----+-----+-----+
    | 1.0 | 2.0 | 3.0 |
    +-----+-----+-----+
    | 4.0 | 5.0 | 6.0 |
    +-----+-----+-----+
    Sheet 3:
    +-----+-----+-----+
    | O   | P   | Q   |
    +-----+-----+-----+
    | 3.0 | 2.0 | 1.0 |
    +-----+-----+-----+
    | 4.0 | 3.0 | 2.0 |
    +-----+-----+-----+
    >>> book.xls  # doctest: +ELLIPSIS
    '...
    >>> book.ods  # doctest: +ELLIPSIS
    '...
    >>> print(book.rst)
    Sheet 1:
    =  =  =
    1  2  3
    4  5  6
    7  8  9
    =  =  =
    Sheet 2:
    ===  ===  ===
    X    Y    Z
    1.0  2.0  3.0
    4.0  5.0  6.0
    ===  ===  ===
    Sheet 3:
    ===  ===  ===
    O    P    Q
    3.0  2.0  1.0
    4.0  3.0  2.0
    ===  ===  ===

Set content
************

Surely, you could set content to an instance of :class:`pyexcel.Book`.

.. code-block:: python

    >>> other_book = pyexcel.Book()
    >>> other_book.bookdict = book_dict
    >>> print(other_book.plain)
    Sheet 1:
    1  2  3
    4  5  6
    7  8  9
    Sheet 2:
    X    Y    Z
    1.0  2.0  3.0
    4.0  5.0  6.0
    Sheet 3:
    O    P    Q
    3.0  2.0  1.0
    4.0  3.0  2.0

You can set via 'xls' attribute too.

.. code-block:: python

    >>> another_book = pyexcel.Book()
    >>> another_book.xls = other_book.xls
    >>> print(another_book.mediawiki)
    Sheet 1:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | align="right"| 1 || align="right"| 2 || align="right"| 3
    |-
    | align="right"| 4 || align="right"| 5 || align="right"| 6
    |-
    | align="right"| 7 || align="right"| 8 || align="right"| 9
    |}
    Sheet 2:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | X || Y || Z
    |-
    | 1 || 2 || 3
    |-
    | 4 || 5 || 6
    |}
    Sheet 3:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | O || P || Q
    |-
    | 3 || 2 || 1
    |-
    | 4 || 3 || 2
    |}


How about setting content via a url?

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

.. code-block:: python

    >>> another_book.url = "https://github.com/pyexcel/pyexcel/raw/master/examples/basics/multiple-sheets-example.xls"
    >>> another_book
    Sheet 1:
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    Sheet 2:
    +---+---+---+
    | X | Y | Z |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet 3:
    +---+---+---+
    | O | P | Q |
    +---+---+---+
    | 3 | 2 | 1 |
    +---+---+---+
    | 4 | 3 | 2 |
    +---+---+---+

.. testcode::
   :hide:

   >>> patcher.stop()


Getters and Setters
----------------------------------

You can pass on source specific parameters to getter and setter functions.

.. code-block:: python

    >>> content = "1-2-3\n3-4-5"
    >>> sheet = pyexcel.Sheet()
    >>> sheet.set_csv(content, delimiter="-")
    >>> sheet.csv
    '1,2,3\r\n3,4,5\r\n'
    >>> sheet.get_csv(delimiter="|")
    '1|2|3\r\n3|4|5\r\n'
