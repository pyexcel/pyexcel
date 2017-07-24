Loading from other sources
================================================================================

.. testcode::
   :hide:

   >>> from mock import patch, MagicMock
   >>> import pyexcel as pe
   >>> patcher = patch('pyexcel._compact.request.urlopen')
   >>> urlopen = patcher.start()
   >>> m = MagicMock()
   >>> x = MagicMock()
   >>> x.type.return_value = "text/csv"
   >>> m.info.return_value = x
   >>> m.read.side_effect = ["1,2,3\n", '']
   >>> urlopen.return_value = m 


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
