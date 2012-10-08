Releases
========

0.89 (2012-10-08)
-----------------

* Fix a problem when the model that you are editing had a Generic Foreign key
* Thanks to `Altimore <https://github.com/altimore>`_

0.88 (2012-10-05)
-----------------

* Add to default parameter to inplace_css
* Translate to the string: "You have unsaved changes!"
* Fix a problem with the treatment of the sizes
* INPLACEEDIT_EDIT_EMPTY_VALUE settings
* Thanks to:
    * `Tobias Birmili <https://github.com/toabi/>`_
    * `Altimore <https://github.com/altimore>`_


0.87 (2012-09-05)
-----------------

* Add callback to onbeforeunload
* Refactor the jquery.inplaceeditform.js
* Now is not required the ADMIN_MEDIA_PREFIX in the settings, but this is backward compatible
* New options to the settings: DEFAULT_INPLACE_EDIT_OPTIONS and DEFAULT_INPLACE_EDIT_OPTIONS_ONE_BY_ONE
* Thanks to:
    * `Tobias Birmili <https://github.com/toabi/>`_
    * `Serpah <https://github.com/serpah/>`_
    * And spatially to `Altimore <https://github.com/altimore>`_


0.86 (2012-08-21)
-----------------

* Toolbar to edit inplace
* Auto save option
* New JS hook (extraConfig)
* Now you can choose the event to edit inplace, by default is doble click
* Now when you edit inline the input (or select) get the focus
* Now while there is a ajax request cannot do other ajax request to the same element
* Update the way to get the CSFRToken
* JSLint to jquery.inplaceeditform.js (There were some errors still)
* Refactor and remove little errors
* Refactor the css files


0.85 (2012-08-09)
-----------------

* A strange error with buildout
* I'm sorry but I removed the package by mistake

0.84 (2012-08-09)
-----------------

* Move the repository to `github <https://github.com/Yaco-Sistemas/django-inplaceedit/>`_

0.83 (2012-05-22)
-----------------

* Now django-inplaceedit managing `static files <https://docs.djangoproject.com/en/dev/howto/static-files/>`_ (backward compatible)

0.82 (2012-03-19)
-----------------
* Fix a error when a field contained "_id"

0.81 (2012-01-25)
-----------------
* A little error in AdminDjangoPermEditInline

0.80 (2012-01-24)
-----------------
* More robust when a user can edit a content
* SuperUserPermEditInline, before was a logic, and you can not inherit.
* AdminDjangoPermEditInline, a logic very useful. Thanks to `Raimon <https://github.com/zikzakmedia/django-inplaceeditform/commit/b6c5427563e77b23494312a7f50c66ba362709b8/>`_

0.79 (2012-01-11)
-----------------
* Messages configurables and translatables in the settings

0.78 (2012-01-9)
----------------
* Messages configurables in the settings

0.77 (2011-12-14)
-----------------
* Fixes a error in bolean adaptor

0.76 (2011-12-08)
-----------------
* More robust

0.75 (2011-11-24)
-----------------
* The resources dont't have dependencie of MEDIA_URL (in CSS file)

0.74 (2011-10-03)
-----------------
* Usability: edit inline works when you submit the form

0.73 (2011-09-22)
-----------------
* Image/File field compatibility with Django 1.1 (overwriting inplaceeditform/adaptor_file/inc.csrf_token.html) (Django 1.2 or above recommended)

0.72 (2011-09-16)
-----------------
* Compatibility with jQuery 1.2 (jQuery 1.5 or above recommended)
* Compatibility with Django 1.1 (Django 1.2 or above recommended)

0.71 (2011-09-5)
----------------
* Fixed error in 0.69 rendering text fields whose font size is not integer.

0.70 (2011-08-31)
-----------------
* Catalonia translations, by Raimon Esteve

0.69 (2011-08-18)
-----------------
* Compatible with the CSRF protection (CsrfViewMiddleware)
* Improvement in the rendering of the widgets (better calculate the height and width)
* More versatile the api

0.68 (2011-08-16)
-----------------
* Update the README

0.67 (2011-06-23)
-----------------
* Spanish translations

0.66 (2011-06-21)
-----------------
* Support to old browsers. Some browser have not a JSON library

0.65 (2011-06-7)
----------------
* Improved the inplace edit widget in images.

0.64 (2011-06-6)
----------------
* Inplace edit of imagefield and filefield works in IE (new), FF, Chrome (alpha)

0.63 (2011-05-24)
-----------------
* Inplace edit of imagefield and filefield (alpha)
* More versatile the api

0.62 (2011-03-18)
-----------------

* Fixes the warning when the error is for other field
* More versatile the api

0.60  (2011-02-18)
------------------

* Created a test project
* Inplace editof booleanfield
* Fixes some details of datetimefield and datefield
* Can't save datetime values on several browser
* The icons did not see
* autoheight and autowidth
* Improve the inplace edit with choices field
* Made less intrusive inplace edit form, now it's putting two spaces)

0.55  (2011-02-11)
------------------

* A new egg from django-inplaceedit-version1
* The js should be a plugin jQuery
* The generated html should be bit intrusive
* API to create adaptators
* Option to auto_height, and auto_width
* Error/ succes messages
* Two functions of render_value, with you can edit, and other when you cannot edit
* A function with empty value
* The files media should not be added if this is adding
* The inplaceedit should can edit some like this:

::

    {% inplace_edit "obj.field_x.field_y" %}
