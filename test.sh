#/bin/bash
pip freeze
coverage run -m --source=pyexcel pytest --doctest-modules && coverage report --show-missing

