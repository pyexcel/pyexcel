========
pyexcel 
========

.. image:: https://api.travis-ci.org/chfw/pyexcel.svg?branch=master
    :target: http://travis-ci.org/chfw/pyexcel

.. image:: https://coveralls.io/repos/chfw/pyexcel/badge.png?branch=master 
    :target: https://coveralls.io/r/chfw/pyexcel?branch=master 

.. image:: https://readthedocs.org/projects/pyexcel/badge/?version=latest
    :target: https://readthedocs.org/projects/pyexcel/?badge=latest

.. image:: https://pypip.in/d/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

.. image:: https://pypip.in/py_versions/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel

.. image:: https://pypip.in/implementation/pyexcel/badge.png
    :target: https://pypi.python.org/pypi/pyexcel
    :alt: Supported Python implementation

**pyexcel** is a wrapper library to read, manipulate and write data in different excel formats: csv, ods, xls, xlsx and xlsm. Its mission is to let you focus on data itself and it deals with different file formats. ODS format support is provided by `pyexcel-ods <https://github.com/chfw/pyexcel-ods>`__ or `pyexcel-ods3 <https://github.com/chfw/pyexcel-ods3>`__. Fonts, colors and charts are not supported.

It was created due to the lack of uniform programming interface to access data in different formats. A developer needs to use different methods of different libraries to read the same data in different excel formats, hence the resulting code is cluttered and unmaintainable.

All great work have done by odf, ezodf(2), xlrd and other individual developers. This library unites only the data access code.

Usage
=====

    >>> import pyexcel as pe
    >>> book = pe.load_book("your_file.xls")
    >>> book.to_dict()
    {"Sheet 1":[[1, 2, 3], ["4", "5", "6"]], "Sheet 2": [["a", "b", "c"], ["e", "f", "g"]], "Sheet 3":[[True, True, False]]}
    >>> # access first sheet's top left cell
    >>> print(book["Sheet 1"]["A1"])
    1
    >>> # alternative access to the same cell
    >>> print(book["Sheet 1"][0,0])
    1   

Documentation
=============

It is hosted in `pyexcel@pyhosted <https://pythonhosted.org/pyexcel/>`_ and `pyexcel@read the docs <https://pyexcel.readthedocs.org/en/latest>`_

Installation
============
You can install it via pip::

    $ pip install pyexcel


or clone it and install it::


    $ git clone http://github.com/chfw/pyexcel.git
    $ cd pyexcel
    $ python setup.py install


Open Document Spreadsheet(ods) Support
-----------------------------------------

In order to add ods support, please choose one of two packages: `pyexcel-ods <https://github.com/chfw/pyexcel-ods>`__ or `pyexcel-ods3 <https://github.com/chfw/pyexcel-ods3>`__ . Please read individual installation instructions respectively. Here is the comparsion of two packages:

============ ========== ========== ========== ========== ==============
package      python 2.6 python 2.7 python 3.3 python 3.4 lxml dependent
============ ========== ========== ========== ========== ==============
pyexcel-ods  yes	    yes	   	   						 no   		  
pyexcel-ods3 		    yes        yes        yes		 yes		      		   	 		   
============ ========== ========== ========== ========== ============== 


Plugin compatibility management
-------------------------------
======= ======== ====== 
pyexcel ods      ods3
======= ======== ======
v0.0.1  n/a      n/a
v0.0.2	                	   
v0.0.3                  		   
v0.0.4  0.0.1    0.0.1
v0.0.5                  		   
v0.0.6  0.0.2    0.0.2
======= ======== ======

Test 
=====

Here is the test command::

    pip install -r tests/requirements.txt
    make test

On Windows, please use::

    test.bat

Test coverage is shown in `codecov.io <https://codecov.io/github/chfw/pyexcel>`_ . For more local test coverage, you can add `--cover-html --cover-html-dir=your_file_directory` to `test.sh` or `test.bat`


Known Issues
=============

* If a zero was typed in a DATE formatted field in xls, you will get "01/01/1900".
* If a zero was typed in a TIME formatted field in xls, you will get "00:00:00".

Acknowledgement
===============

Extension management code was copied from `flask <https://github.com/mitsuhiko/flask>`_. 
