cd tests\test_plugin
python setup.py install
cd ..\..\
nosetests --with-doctest --doctest-extension=.rst doc/source pyexcel tests  README.rst
del tmp.db
