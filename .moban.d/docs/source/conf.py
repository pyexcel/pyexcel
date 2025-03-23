{% extends 'docs/source/conf.py.jj2'%}

{%block SPHINX_EXTENSIONS%}
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinxcontrib.excel'
{%endblock%}

{%block custom_doc_theme%}
def setup(app):
    app.add_stylesheet('theme_overrides.css')


{%endblock%}

{%block additional_mapping%}
    'xlrd': ('http://xlrd.readthedocs.io/en/latest/', None)
{%endblock%}
