{% extends 'setup.py.jj2' %}

{%block compat_block%}
from pyexcel._compact import PY2, PY26
{%endblock%}

{% block additional_keywords %}
    'tsv',
    'tsvz'
    'csv',
    'csvz',
    'xls',
    'xlsx',
    'ods'
{% endblock %}

{% block additional_classifiers %}
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy'
{% endblock %}}

