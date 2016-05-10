#/bin/bash

cd tests/test_plugin
python setup.py install
cd ../../

{% include "test.sh.jj2" %}

if [ $? == 0 ] ; then
	rm tmp.db
else
    rm tmp.db
    exit 1;
fi
