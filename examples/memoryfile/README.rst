=============================
Dealing with files in memory
=============================

This is an example of handling excel file in web development environment. Instead of saving the uploaded file, pyexcel enables loading it from memory.

Installation
=============

You will need the html file in templates directory and keep the directory structure. Then please install Flask in addition::

    $ pip install Flask

After that, you can launch the mini server::

    $ python pyexcel_server.py

Then visit http://localhost:5000/upload or http://localhost:5000/download

Relevant packages
=================

Readily made plugins have been made on top of this example. Here is a list of them:

============== ============================
framework      plugin/middleware/extension
============== ============================
Flask          `Flask-Excel`_
Django         `django-excel`_
Pyramid        `pyramid-excel`_
============== ============================

.. _Flask-Excel: https://github.com/chfw/Flask-Excel
.. _django-excel: https://github.com/chfw/django-excel
.. _pyramid-excel: https://github.com/chfw/pyramid-excel

And you may make your own by using `pyexcel-webio <https://github.com/chfw/pyexcel-webio>`_
