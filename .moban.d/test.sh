{% extends "test.sh.jj2" %}

{%block pretest %}
#/bin/bash

cd tests/test_plugin
python setup.py install
cd ../../
{%endblock %}

{%block flake8_options%}
--builtins=unicode,xrange,long
{%endblock%}
