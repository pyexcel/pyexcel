python setup.py install
nosetests --with-cov --with-doctest --doctest-extension=.rst doc/source pyexcel tests
del tmp.db
