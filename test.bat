cd tests\test_plugin
python setup.py install
cd ..\pyexcel-presentation
python setup.py install
cd ..\..\
nosetests --with-cov --with-doctest --doctest-extension=.rst doc/source pyexcel tests
del tmp.db
