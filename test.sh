#/bin/bash

cd tests/test_plugin
python setup.py install
cd ../../


pip freeze
nosetests --with-cov --cover-package pyexcel --cover-package tests --with-doctest --doctest-extension=.rst tests README.rst docs/source pyexcel && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long

