{% extends "test.sh.jj2" %}

{%block flake8_options%}
--builtins=unicode,xrange,long
{%endblock%}



