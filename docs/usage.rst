.. _usage:

=====
Usage
=====

Calling `inplace_edit tag <https://github.com/Yaco-Sistemas/django-inplaceedit/blob/master/inplaceeditform/templatetags/inplace_edit.py/>`_ you can inplace edit any data from the database. It is important to clarify that the inline edition is not only for text fields, although it may be the more common usage. You can also have inline edition for choices, boolean fields, date and datetime fields, foreing keys, many to many, file and image fields.

::

  {% inplace_edit  "OBJ.FIELD_NAME" %}
  {% inplace_edit  "OBJ.FIELD_NAME|FILTER1|FILTER2|...|FILTERN" %}

Example
=======

::

 {% load inplace_edit %}
    <html>
    <head>
    ...
    <script src="{{ STATIC_URL }}js/jquery.min.js" type="text/javascript"></script>
    {% inplace_toolbar %}
    </head>
    <body>
        ...
        <div id="content">
            ...
            {% inplace_edit "content.name" %}
            ...
            <div class="description">
                {% inplace_edit "content.date_initial|date:'d m Y'" %}
                {% inplace_edit "content.description|safe" %}
            </div>
            <div class="body">
                {% inplace_edit "content.body|safe|truncatewords_html:15" %}
            </div>
        </div>
        ...
    </body>
    </html>

How to use it
-------------

 * If you use `inplace_static <https://github.com/Yaco-Sistemas/django-inplaceedit/blob/master/inplaceeditform/templatetags/inplace_edit.py/>`_: Just pass the cursor above the field and double click (this is :ref:`customizable <customize>`), authenticated with a super user (this is also :ref:`customizable <customize>`)
 * If you use `inplace_toolbar <https://github.com/Yaco-Sistemas/django-inplaceedit/blob/master/inplaceeditform/templatetags/inplace_edit.py/>`_: Enable a edit inline and just pass the cursor above the field and double click (this is :ref:`customizable <customize>`), authenticated with a super user (this is also :ref:`customizable <customize>`)