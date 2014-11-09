cd tests\test_plugin
python setup.py install
cd ..\..\
nosetests --rednose --with-cov --with-doctest --doctest-extension=.rst tests doc\source pyexcel
