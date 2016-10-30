python setup.py clean --all
python setup.py install
del docs\source\generated\*.rst
del docs\source\iapi\*.rst
sphinx-autogen -o docs\source\generated docs\source\api.rst
sphinx-autogen -o docs\source\iapi docs\source\iapi.rst
sphinx-build -b html docs\source docs\build
