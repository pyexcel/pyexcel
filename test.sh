#/bin/bash
python setup.py install
nosetests --rednose --with-cov --with-doctest --doctest-extension=.rst doc/source pyexcel tests
rm tmp.db
