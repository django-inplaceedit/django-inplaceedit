django-inplaceedit test project
=================================
Project to reproduce errors for others to debug it.

default login : test
default password : testtest

Howto
======

Create a virtual env

::

    $ virtualenv virt-inplaceedit

Get in and activate the env

::

    $ source virt-inplaceedit/bin/activate

Install the required packages

::

    $ pip install Django
    $ pip install Pillow (the version depends on your Python version)
    $ python setup.py develop
    $ cd testing
    $ pip install -r requirements.txt

Install django-transmeta, if you want test this integration

::

    $ pip install django-transmeta

Install django-inplaceedit-extra-fields and its dependencies, if you want test this integration (sorl-thumbnail and django-ajax-selects)

::

    $ pip install django-inplaceedit-extra-fields sorl-thumbnail==12.3 django-ajax-selects==1.3.6

Create db and load fixtures

::

    python manage.py migrate (syncdb if you are useing a old Django version)

Start the debug server

::

    $ ./manage.py runserver

Do your stuffs
