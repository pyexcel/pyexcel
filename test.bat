
cd tests\test_plugin
python setup.py install
cd ..\..\
nosetests --with-cov --with-doctest --doctest-extension=.rst tests doc\source pyexcel
