
======================
Internal API reference
======================

.. currentmodule:: pyexcel.sheets
.. _iapi:

This is intended for developers and hackers of pyexcel. 


Data sheet representation
=========================

In inheritance order from parent to child

.. autosummary::
   :toctree: iapi/

   Matrix
   
.. autosummary::
   :toctree: iapi/

   FormattableSheet
   FilterableSheet
   NominableSheet
   Sheet

Row represetation
===================

.. autosummary::
   :toctree: iapi/

   Row

Column represetation
=====================

.. autosummary::
   :toctree: iapi/

   Column

File type handlers
==================

New file type handlers are registered via two internal static dictionaries: READERS for file readers, and WRITERS for file writers

.. currentmodule:: pyexcel.io
.. autosummary::
   :toctree: iapi/

   load_file
   get_writer
