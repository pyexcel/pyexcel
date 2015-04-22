Developer's guide
=================

Here's the architecture of pyexcel

.. image:: architecture.png

Pull requests are welcome.

Acceptance criteria
-------------------

#. Has fair amount of documentation
#. Has Test cases written
#. Has all code lines tested
#. Passes all Travis CI builds
#. Pythonic code please
#. Agree on NEW BSD License for your contribution

How to test your contribution
------------------------------

Although `nose` and `doctest` are both used in code testing, it is adviable that unit tests are put in tests. `doctest` is incorporated only to make sure the code examples in documentation remain valid across different development releases.

On Linux/Unix systems, please launch your tests like this::

    $ make test

On Windows systems, please issue this command::

    > test.bat

