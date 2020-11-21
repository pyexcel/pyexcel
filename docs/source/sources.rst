Loading from other sources
================================================================================

Get back into pyexcel
++++++++++++++++++++++++++++++++

list
********************************************************************************

.. code-block :: python

    >>> import pyexcel as p
    >>> two_dimensional_list = [
    ...    [1, 2, 3, 4],
    ...    [5, 6, 7, 8],
    ...    [9, 10, 11, 12],
    ... ]
    >>> sheet = p.get_sheet(array=two_dimensional_list)
    >>> sheet
    pyexcel_sheet1:
    +---+----+----+----+
    | 1 | 2  | 3  | 4  |
    +---+----+----+----+
    | 5 | 6  | 7  | 8  |
    +---+----+----+----+
    | 9 | 10 | 11 | 12 |
    +---+----+----+----+

dict
***********

.. code-block :: python

    >>> a_dictionary_of_key_value_pair = {
    ...    "IE": 0.2,
    ...    "Firefox": 0.3
    ... }
    >>> sheet = p.get_sheet(adict=a_dictionary_of_key_value_pair)
    >>> sheet
    pyexcel_sheet1:
    +---------+-----+
    | Firefox | IE  |
    +---------+-----+
    | 0.3     | 0.2 |
    +---------+-----+

.. code-block :: python

    >>> a_dictionary_of_one_dimensional_arrays = {
    ...     "Column 1": [1, 2, 3, 4],
    ...     "Column 2": [5, 6, 7, 8],
    ...     "Column 3": [9, 10, 11, 12],
    ... }
    >>> sheet = p.get_sheet(adict=a_dictionary_of_one_dimensional_arrays)
    >>> sheet
    pyexcel_sheet1:
    +----------+----------+----------+
    | Column 1 | Column 2 | Column 3 |
    +----------+----------+----------+
    | 1        | 5        | 9        |
    +----------+----------+----------+
    | 2        | 6        | 10       |
    +----------+----------+----------+
    | 3        | 7        | 11       |
    +----------+----------+----------+
    | 4        | 8        | 12       |
    +----------+----------+----------+

records
*************

.. code-block :: python

    >>> a_list_of_dictionaries = [
    ...     {
    ...         "Name": 'Adam',
    ...         "Age": 28
    ...     },
    ...     {
    ...         "Name": 'Beatrice',
    ...         "Age": 29
    ...     },
    ...     {
    ...         "Name": 'Ceri',
    ...         "Age": 30
    ...     },
    ...     {
    ...         "Name": 'Dean',
    ...         "Age": 26
    ...     }
    ... ]
    >>> sheet = p.get_sheet(records=a_list_of_dictionaries)
    >>> sheet
    pyexcel_sheet1:
    +-----+----------+
    | Age | Name     |
    +-----+----------+
    | 28  | Adam     |
    +-----+----------+
    | 29  | Beatrice |
    +-----+----------+
    | 30  | Ceri     |
    +-----+----------+
    | 26  | Dean     |
    +-----+----------+

book dict
**************

.. code-block :: python

    >>> a_dictionary_of_two_dimensional_arrays = {
    ...      'Sheet 1':
    ...          [
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0],
    ...              [7.0, 8.0, 9.0]
    ...          ],
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
    ...          ]
    ...  }
    >>> book = p.get_book(bookdict=a_dictionary_of_two_dimensional_arrays)
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



.. testcode::
   :hide:

   >>> from unittest.mock import patch, MagicMock
   >>> import pyexcel as pe
   >>> from pyexcel._compact import StringIO, PY2, BytesIO
   >>> patcher = patch('pyexcel._compact.request.urlopen')
   >>> urlopen = patcher.start()
   >>> io = StringIO("1,2,3") if PY2 else BytesIO("1,2,3".encode('utf-8'))
   >>> x = MagicMock()
   >>> x.type.return_value = "text/csv"
   >>> io.info = x
   >>> urlopen.return_value = io


How to load a sheet from a url
--------------------------------------------------------------------------------

Suppose you have excel file somewhere hosted::

   >>> sheet = pe.get_sheet(url='http://yourdomain.com/test.csv')
   >>> sheet
   csv:
   +---+---+---+
   | 1 | 2 | 3 |
   +---+---+---+


.. testcode::
   :hide:

   >>> patcher.stop()  # doctest: +SKIP


For sheet
--------------------------------------------------------------------------------

Get content
************

.. testcode::
   :hide:

   >>> from unittest.mock import patch, MagicMock
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

   >>> another_sheet = p.Sheet()
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

   >>> patcher.stop()  # doctest: +SKIP

   
For book
--------------------------------------------------------------------------------

How about setting content via a url?

.. testcode::
   :hide:

   >>> from unittest.mock import patch, MagicMock
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

    >>> another_book = p.Book()
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

   >>> patcher.stop()  # doctest: +SKIP
