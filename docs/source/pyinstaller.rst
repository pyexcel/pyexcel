Packaging with PyInstaller
================================================================================

With pyexcel v0.5.0, the way to package it has been changed because it
uses lml for all plugins.

And you need to do the same for `pyexcel-io plugins <http://pyexcel-io.readthedocs.io/en/latest/pyinstaller.html>`_ too.

Built-in plugins of pyexcel
-------------------------------

In order to package every built-in plugins of pyexcel-io, you need to specify::

    --hidden-import pyexcel.plugins.renderers.sqlalchemy
    --hidden-import pyexcel.plugins.renderers.django
    --hidden-import pyexcel.plugins.renderers.excel
    --hidden-import pyexcel.plugins.renderers._texttable
    --hidden-import pyexcel.plugins.parsers.excel
    --hidden-import pyexcel.plugins.parsers.sqlalchemy
    --hidden-import pyexcel.plugins.sources.http
    --hidden-import pyexcel.plugins.sources.file_input
    --hidden-import pyexcel.plugins.sources.memory_input
    --hidden-import pyexcel.plugins.sources.file_output
    --hidden-import pyexcel.plugins.sources.output_to_memory
    --hidden-import pyexcel.plugins.sources.pydata.bookdict
    --hidden-import pyexcel.plugins.sources.pydata.dictsource
    --hidden-import pyexcel.plugins.sources.pydata.arraysource
    --hidden-import pyexcel.plugins.sources.pydata.records
    --hidden-import pyexcel.plugins.sources.django
    --hidden-import pyexcel.plugins.sources.sqlalchemy
    --hidden-import pyexcel.plugins.sources.querysets
