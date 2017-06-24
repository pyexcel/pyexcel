Architecture
===============

**pyexcel** uses loosely couple plugins to fullfil the promise to access
various file formats. **lml** is the plugin management library that
provide the specialized support for the loose coupling.

What is loose coupling?
-------------------------

The components of **pyexcel** is designed as building blocks. For your
project, you can cherry-pick the file format support without affecting
the core functionality of pyexcel. Each plugin will bring in additional
dependences. For example, if you choose pyexcel-xls, xlrd and xlwt will
be brought in as 2nd level depndencies.

Looking at the following architectural diagram, pyexcel hosts plugin
interfaces for data source, data renderer and data parser. pyexel-pygal,
pyexcel-matplotlib, and pyexce-handsontable extend pyexcel using data
renderer interface. pyexcel-io package takes away the responsibilities
to interface with excel libraries, for example: xlrd, openpyxl, ezodf.

As in :ref:`a-map-of-plugins-and-file-formats`, there are overlapping
capabilities in reading and writing xlsx, ods files. Because each
third parties express different personalities although they may
read and write data in the same file format, you as the pyexcel is
left to pick which suit your task best.

Dotted arrow means the package or module is loaded later.

.. image:: _static/images/architecture.svg

