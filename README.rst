Peak
====

Aptitude test.


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ docker-compose -f local.yml run --rm django coverage run -m pytest
    $ docker-compose -f local.yml run --rm django coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    $ docker-compose -f local.yml run --rm django pytest

Deployment
----------
The following details how to deploy this application.

* Rename ".envs_templates" and change envs values to your own::

    $ mv .envs_templates/ .envs

* Build images::

    $ docker-compose -f local.yml build

* Migrate::

    $ docker-compose -f local.yml run --rm django python3 manage.py makemigrations
    $ docker-compose -f local.yml run --rm django python3 manage.py migrate

* Populate models. Can take ~5 minutes::

    $ docker-compose -f local.yml run --rm django python3 manage.py cities_light

* Run images::

    $ docker-compose -f local.yml up

* Check http://0.0.0.0:8000/
