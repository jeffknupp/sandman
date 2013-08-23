.PHONY: docs test release

test:
		coverage run --source=sandman setup.py test && \
		coverage html && \
		coverage report

docs:
	sphinx-build -aE docs docs/generated > /dev/null

release: test docs
	open docs/generated/index.html
	open htmlcov/index.html
	vim sandman/__init__.py
