Loading from other sources
================================================================================

.. testcode::
   :hide:

   >>> from mock import patch, MagicMock
   >>> import pyexcel as pe
   >>> from pyexcel._compact import StringIO
   >>> patcher = patch('pyexcel._compact.request.urlopen')
   >>> urlopen = patcher.start()
   >>> io = StringIO("1,2,3")
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

   >>> patcher.stop()
