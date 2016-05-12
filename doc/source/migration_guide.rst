Migrate from 0.2.1 to 0.2.2
================================

1. Explicit imports, no longer needed
--------------------------------------------

Please forget about these statements::

    import pyexcel.ext.xls
	import pyexcel.ext.ods
	import pyexcel.ext.xlsx

They are no longer needed. As long as you have pip-installed them, they will
be auto-loaded.

2. Invalid environment marker: platform_python_implementation=="PyPy"
-----------------------------------------------------------------------

Yes, it is a surprise. Please upgrade setuptools in your environment::

    pip install --upgrade setuptools

At the time of writing, setuptools (18.0.1) or setuptools-21.0.0-py2.py3-none-any.whl is installed on author's computer and worked.


Migrate from 0.1.x to 0.2.x
===============================

1. "Writer" is gone, Please use save_as.
-------------------------------------------

.. testcode::
   :hide:

    >>> import pyexcel

Here is a piece of legacy code:

.. code-block:: python

    w = pyexcel.Writer("afile.csv")
    data=[['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]]
    w.write_array(table)
    w.close()

The new code is:

.. code-block:: python

    >>> data=[['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]]
    >>> pyexcel.save_as(array=data, dest_file_name="afile.csv")

.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("afile.csv")


Here is another piece of legacy code:

.. code-block:: python

    content = {
        "X": [1,2,3,4,5],
        "Y": [6,7,8,9,10],
        "Z": [11,12,13,14,15],
    }
    w = pyexcel.Writer("afile.csv")
    w.write_dict(self.content)
    w.close()

The new code is:

.. code-block:: python

   >>> content = {
   ...     "X": [1,2,3,4,5],
   ...     "Y": [6,7,8,9,10],
   ...     "Z": [11,12,13,14,15],
   ... }
   >>> pyexcel.save_as(adict=content, dest_file_name="afile.csv")

   
.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("afile.csv")

Here is yet another piece of legacy code:

.. code-block:: python

    data = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    io = StringIO()
    w = pyexcel.Writer(("csv",io))
    w.write_rows(data)
    w.close()

The new code is:

    
    >>> data = [
    ...     [1, 2, 3],
    ...     [4, 5, 6]
    ... ]
    >>> io = pyexcel.save_as(dest_file_type='csv', array=data)
    >>> for line in io.readlines():
    ...     print(line.rstrip())
    1,2,3
    4,5,6
    
2. "BookWriter" is gone. Please use save_book_as.
---------------------------------------------------

Here is a piece of legacy code:

.. code-block:: python

   import pyexcel
   content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
   w = pyexcel.BookWriter("afile.csv")
   w.write_book_from_dict(content)
   w.close()


The replacement code is:

.. code-block:: python

   >>> import pyexcel
   >>> content = {
   ...          "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
   ...          "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
   ...          "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
   ...      }
   >>> pyexcel.save_book_as(bookdict=content, dest_file_name="afile.csv")

.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("afile__Sheet1__0.csv")
    >>> os.unlink("afile__Sheet2__1.csv")
    >>> os.unlink("afile__Sheet3__2.csv")

