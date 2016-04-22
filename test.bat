cd tests\test_plugin
python setup.py install
cd ..\..\
nosetests --with-doctest --doctest-extension=.rst doc/source pyexcel tests --with-cov --cov examples --cov pyexcel --cov tests 
del tmp.db
