#/bin/bash
pip freeze

cd tests/test_plugin
python setup.py install
cd ../../
nosetests --with-cov --cov examples --cov pyexcel --cov tests --with-doctest --doctest-extension=.rst doc/source pyexcel tests
if [ $? == 0 ] ; then
	rm tmp.db
else
    rm tmp.db
    exit 1;
fi
