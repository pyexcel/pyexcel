cd tests\test_plugin
python setup.py install
cd ..\pyexcel-presentation
python setup.py install
cd ..\..\
nosetests --with-doctest --doctest-extension=.rst doc/source pyexcel tests --with-cov --cov examples --cov pyexcel --cov tests --cov-report html
del tmp.db
