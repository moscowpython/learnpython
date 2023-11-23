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
run:
	cd landing_page; DEBUG=1 python manage.py runserver
shell:
	cd landing_page; DEBUG=1 python manage.py shell
migrate:
	cd landing_page; DEBUG=1 python manage.py migrate
