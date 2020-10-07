all: test

test: lint
	bash test.sh

install_test:
	pip install -r tests/requirements.txt

lint:
	bash lint.sh

format:
	bash format.sh

git-diff-check:
	git diff --exit-code
