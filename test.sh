#/bin/bash

cd tests/test_plugin
python setup.py install
cd ../../
nosetests --rednose --with-cov
