# To setup project localy

* Set up virtualenv
* Install requirements from `requirements.txt`
* Change settings in `settings.py`
* Run migrations and start the project with `python manage.py runserver`

# To deploy project

Check the `fabfile.py` if you need to alter deployment settings. Then install requirements from requitements-deploy.txt and run `fab deploy`