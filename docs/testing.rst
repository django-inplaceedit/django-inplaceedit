.. _testing:

=======
Testing
=======

This django application has been tested on severals browsers: Firefox, Google Chrome, Opera, Safari and Internet Explorer on versions 7, 8, 9 and 10 to check javascript actions. **Attention**, `jQuery 2 <http://blog.jquery.com/2013/04/18/jquery-2-0-released/>`_ does not support IE 6/7/8. If you want to test in these browsers, please use jQuery 1 (recomended the last release 1.10.2)

Exists a `testing django project <https://github.com/Yaco-Sistemas/django-inplaceedit/tree/master/testing/>`_. This project can use as demo project, because django-inplaceedit is totally adapted to it.

Also you can use the demo project of `django-inplaceedit-bootstrap <https://github.com/goinnn/django-inplaceedit-bootstrap/tree/master/testing>`_

The backend has `unit test <https://travis-ci.org/Yaco-Sistemas/django-inplaceedit/>`_, to check it.::

    cd testing
    python run_tests.py

You can see this django-inplaceedit works (without changes) from django 1.2, and even in previous versions of Django (1.1 and 1.0) works with some customizations.
