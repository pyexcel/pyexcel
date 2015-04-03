====================================
File formats: .csvz and .tsvz
====================================

.. _csvz:

Introduction
-------------

'csvz' and 'tsvz' are newly invented excel file formats by pyexcel. Simply put, 'csvz' is the zipped content of one or more csv file(s). 'tsvz' is the twin brother of 'csvz'. They are similiar to the implementation of xlsx format, which is a zip of excel content in xml format.

The obvious tangile benefit of zipped csv over normal csv is the reduced file size. However, the drawback is the need of unzipping software.

Single Sheet
------------

When a single sheet is to be saved, the resulting csvz file will be a zip file that contains one csv file bearing the name of :class:`~pyexcel.Sheet`.

    >>> import pyexcel as pe
    >>> data = [[1,2,3]]
    >>> sheet = pe.Sheet(data)
    >>> sheet.save_as("myfile.csvz")
    >>> import zipfile
    >>> zip = zipfile.ZipFile("myfile.csvz", 'r')
    >>> zip.namelist()
    ['pyexcel.csv']
    >>> zip.close()

And it can be read out as well and can be saved in any other supported format.

    >>> sheet2 = pe.get_sheet(file_name="myfile.csvz")
    >>> sheet2
    Sheet Name: pyexcel
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+


Multiple Sheet Book
-------------------

When multiple sheets are to be saved as a book, the resulting csvz file will be a zip file that contains each sheet as a csv file named after corresponding sheet name.

    >>> content = {
    ...     'Sheet 1': 
    ...         [
    ...             [1.0, 2.0, 3.0], 
    ...             [4.0, 5.0, 6.0], 
    ...             [7.0, 8.0, 9.0]
    ...         ],
    ...     'Sheet 2': 
    ...         [
    ...             ['X', 'Y', 'Z'], 
    ...             [1.0, 2.0, 3.0], 
    ...             [4.0, 5.0, 6.0]
    ...         ], 
    ...     'Sheet 3': 
    ...         [
    ...             ['O', 'P', 'Q'], 
    ...             [3.0, 2.0, 1.0], 
    ...             [4.0, 3.0, 2.0]
    ...         ] 
    ... }
    >>> book = pe.Book(content)
    >>> book.save_as("mybook.csvz")
    >>> import zipfile
    >>> zip = zipfile.ZipFile("mybook.csvz", 'r')
    >>> zip.namelist()
    ['Sheet 1.csv', 'Sheet 2.csv', 'Sheet 3.csv']
    >>> zip.close()

The csvz book can be read back with two lines of code. And once it is read out, it can be saved in any other supported format.

    >>> book2 = pe.get_book(file_name="mybook.csvz")
    >>> book2
    Sheet Name: Sheet 1
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    Sheet Name: Sheet 2
    +---+---+---+
    | X | Y | Z |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    Sheet Name: Sheet 3
    +---+---+---+
    | O | P | Q |
    +---+---+---+
    | 3 | 2 | 1 |
    +---+---+---+
    | 4 | 3 | 2 |
    +---+---+---+


Open csvz without pyexcel
----------------------------

All you need is a unzipping software. I would recommend 7zip which is open source and is available on all available OS platforms.

On latest Windows platform (windows 8), zip file is supported so just give the "csvz" file a file extension as ".zip". The file can be opened by File Explorer.


.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("myfile.csvz")
    >>> os.unlink("mybook.csvz")
