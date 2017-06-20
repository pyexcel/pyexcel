# -*- coding: utf-8 -*-
DESCRIPTION = (
    'A wrapper library that provides one API to read, manipulate and write ' +
    'data in different excel formats' +
    ''
)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinxcontrib.spelling',
    'sphinxcontrib.excel'
]

intersphinx_mapping = {
    'xlrd': ('http://xlrd.readthedocs.io/en/latest/', None)
}
spelling_word_list_filename = 'spelling_wordlist.txt'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'pyexcel'
copyright = u'2015-2017 Onni Software Ltd.'
version = '0.5.0'
release = '0.5.0'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'


def setup(app):
    app.add_stylesheet('theme_overrides.css')


html_static_path = ['_static']
htmlhelp_basename = 'pyexceldoc'
latex_elements = {}
latex_documents = [
    ('index', 'pyexcel.tex',
     'pyexcel Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'pyexcel',
     'pyexcel Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'pyexcel',
     'pyexcel Documentation',
     'Onni Software Ltd.', 'pyexcel',
     DESCRIPTION,
     'Miscellaneous'),
]
