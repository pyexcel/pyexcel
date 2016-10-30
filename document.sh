python setup.py install
rm docs/source/generated/*.rst
rm docs/source/iapi/*.rst
sphinx-autogen -o docs/source/generated docs/source/api.rst
sphinx-autogen -o docs/source/iapi docs/source/iapi.rst
sphinx-build -b html docs/source docs/build
