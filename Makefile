.PHONY: docs release clean build

clean:
	rm -rf sandman_env htmlcov

build:
	virtualenv sandman_env && source sandman_env/bin/activate && \
		pip install -r requirements.txt

test: clean build
		source sandman_env/bin/activate && \
		coverage run --source=sandman setup.py test && \
		coverage html && \
		coverage report

docs:
	sphinx-build -aE docs docs/generated > /dev/null

release: test docs
	open docs/generated/index.html
	open htmlcov/index.html
	vim sandman/__init__.py
