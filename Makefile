isort:
	isort .
style:
	flake8 .
types:
	mypy .
test:
	cd landing_page; pytest .
check:
	make isort style types test
