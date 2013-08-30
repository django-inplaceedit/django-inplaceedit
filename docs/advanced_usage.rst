.. _advanced_usage:

==============
Advanced Usage
==============

Inplaceedit has some optionals parameters that the templatetag can receive to change its behavior:
 * auto_height: Adapt the height's widget to the tag container.
 * auto_width: Adapt the width's widget to the tag container.
 * min_width: The minimum of the width's widget
 * class_inplace: Add a class to edit inline form.
 * tag_name_cover: The value is covered for a span. But it's possible to change it.
 * filters_to_show: The server filters the value before to save. List separate for "|"
 * loads: If you use some filter that need a load, you set this option. List separate for ":"
 * edit_empty_value: The text to display when the field is empty

Examples
--------

::

    {% inplace_edit "content.description|safe" auto_height=1, auto_width=1 %}
    {% inplace_edit "content.title" class_inplace="titleFormEditInline" %}
    {% inplace_edit "content.description|safe" filters_to_show="safe|truncatewords_html:30", tag_name_cover="div" %}
    {% inplace_edit "content.description|my_filter" loads="my_template_tag" %}
    {% inplace_edit "content.index" edit_empty_value="This is a editable content, now the value is none. Please double click to edit inplace" %}
    {% inplace_edit "content.amount" min_width="100" %}
