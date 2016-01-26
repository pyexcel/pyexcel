{% extends 'docs/source/conf.py.jj2'%}

{%block custom_doc_theme%}
html_theme = 'default'
def setup(app):
    app.add_stylesheet('theme_overrides.css')
{%endblock%}

