.. _getting_started:

===============
Getting started
===============

Information
===========

Inplace Edit Form is a Django application that allows you to inline edition of some data from the database

It is distributed under the terms of the GNU Lesser General Public
License <http://www.gnu.org/licenses/lgpl.html>

Demo
====

Video Demo, of django-inplaceedit and `Django-inlinetrans <http://pypi.python.org/pypi/django-inlinetrans>`_ (Set full screen mode to view it correctly)

.. image:: https://github.com/django-inplaceedit/django-inplaceedit/raw/master/video-frame.png
   :target: http://youtu.be/_EjisXtMy_Y?t=34s

Usage
=====

Calling `inplace_edit tag <https://github.com/Yaco-Sistemas/django-inplaceedit/blob/master/inplaceeditform/templatetags/inplace_edit.py/>`_ you can inplace edit any data from the database. It is important to clarify that the inline edition is not only for text fields, although it may be the more common usage. You can also have inline edition for choices, boolean fields, date and datetime fields, foreing keys, many to many, file and image fields.

::

  {% inplace_edit  "OBJ.FIELD_NAME" %}
  {% inplace_edit  "OBJ.FIELD_NAME|FILTER1|FILTER2|...|FILTERN" %}

You only should change this:

::

  <span>{{ user.first_name }}</span>
  <span>{{ user.last_name }}</span>


to this:

::

  <span>{% inplace_edit  "user.first_name" %}</span>
  <span>{% inplace_edit  "user.last_name" %}</span>
