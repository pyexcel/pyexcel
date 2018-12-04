all: test

test:
	bash test.sh

doc:
	bash document.sh

uml:
	plantuml -tsvg -o ../_static/images/ docs/source/uml/*.uml

format:
	isort -y $(find pyexcel -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
	black -l 79 pyexcel
	black -l 79 tests
