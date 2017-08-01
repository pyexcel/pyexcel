How to write a plugin for pyexcel
================================================================================

.. note::

   Under writing. Stay tuned.

There are three types of plugins for pyexcel: data parser, data renderer and
data source.

Tutorial
--------------------------------------------------------------------------------

Let me walk you through the process of creating pyexcel-pdfr package.

Prerequisites:

#. pip install moban yehua
#. git clone https://github.com/moremoban/setupmobans.git # generic setup
#. git clone https://github.com/pyexcel/pyexcel-commons.git

Let me assume that you have the work directory as::

    setupmobans pyexcel-commons

and `YOUR_WORK_DIRECTORY` points to the base directory for both.

And then please export an environment variable::

    export YEHUA_FILE=$YOUR_WORK_DIRECTORY/pyexcel-commons/yehua/yehua.yml

Now let's get started.

Step 1
********************************************************************************

Call `yehua` to get the basic scaffolding::

    $ yehua
    Yehua will walk you through creating a pyexcel package.
    Press ^C to quit at any time.
    
    What is your project name? pyexcel-pdfr
    What is the description? parses tables in pdf file as tabular data
    What is project type?
    1. pyexcel plugins
    2. command line interface
    3. python's C externsion
    (1,2,3): 1
    What is the nick name? pdf
    $

Step 2
********************************************************************************

Call `moban` to inflate all project files::

    $ cd pyexcel-pdfr/
    $ ln -s ../pyexcel-commons/ commons
    $ ln -s ../setupmobans/ setupmobans
    $ moban
    Templating README.rst to README.rst
    Templating setup.py to setup.py
    Templating requirements.txt to requirements.txt
    Templating NEW_BSD_LICENSE.jj2 to LICENSE
    Templating MANIFEST.in.jj2 to MANIFEST.in
    Templating tests/requirements.txt to tests/requirements.txt
    Templating test.script.jj2 to test.sh
    Templating test.script.jj2 to test.bat
    Templating travis.yml.jj2 to .travis.yml
    Templating gitignore.jj2 to .gitignore
    Templating docs/source/conf.py.jj2 to docs/source/conf.py

Step 3 - Coding
********************************************************************************

Please put your code in pyexcel_pdfr

