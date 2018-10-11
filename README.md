# To setup project localy

* Setup **virtualenv**
* Install requirements from `requirements.txt`
   `pip install -r requirements.txt`
* Change settings in `settings.py`
* Go to sub directory `landing_page` in terminal
    `cd learnpython/landing_page`
* Run migrations `python manage.py migrate`
* Add admin user `python manage.py createsuperuser`
* Install and start the **redis-server**
    `sudo apt-get install redis-server`
    `sudo service redis-server start`
* Running workers
    **django_rq** provides a management command that starts a worker for every
    queue specified as arguments:
    `python manage.py rqworker default`

# Start using project localy

* Start the project with `python manage.py runserver`
* Login to the Admin panel in a browser `http://127.0.0.1:8000/admin/`
![Inside the Admin panel](img/enter_admin.jpg)
* Create enrollment.
![Create enrollment example](img/create_enrollment.jpg)

# To deploy project

Check the `fabfile.py` if you need to alter deployment settings. Then install requirements from requitements-deploy.txt and run `fab deploy`
