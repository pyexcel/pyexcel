#/bin/bash

cd tests/test_plugin
python setup.py install
cd ../pyexcel-presentation
python setup.py install
cd ../../
nosetests --rednose --with-cov --with-doctest --doctest-extension=.rst doc/source pyexcel tests
if [ $? == 0 ] ; then
	rm tmp.db
else
    exit 1;
fi
