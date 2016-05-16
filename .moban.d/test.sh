#/bin/bash

cd tests/test_plugin
python setup.py install
cd ../../

{% include "test.sh.jj2" %}
