.. _install:

=======
Install
=======

Requirements
============

 * `Django <https://www.djangoproject.com/>`_ (>= 1.2, even works with 1.1 with some customizations in your project)
 * `jQuery <http://jquery.com/>`_ (>=1.5.0)



In your base.html
=================

Add ::

    {% load inplace_edit %}

and wherever you load your static files, add either ::

    {% inplace_toolbar %}

or ::

    {% inplace_static %}


In your settings.py
===================

::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',

        #.....................#

        'inplaceeditform',
    )


And uncomment the request context processor:

::

    TEMPLATE_CONTEXT_PROCESSORS = (
        #...#
        'django.core.context_processors.request',
        #...#
    )


Optional:

::

    INPLACEEDIT_EDIT_EMPTY_VALUE = 'Double click to edit'
    INPLACEEDIT_AUTO_SAVE = True
    INPLACEEDIT_EVENT = "dblclick"
    INPLACEEDIT_DISABLE_CLICK = True  # For inplace edit text into a link tag
    INPLACEEDIT_EDIT_MESSAGE_TRANSLATION = 'Write a translation' # transmeta option
    DEFAULT_INPLACE_EDIT_OPTIONS = {} # dictionnary of the optionals parameters that the templatetag can receive to change its behavior (see the Advanced usage section)
    DEFAULT_INPLACE_EDIT_OPTIONS_ONE_BY_ONE = True # modify the behavior of the DEFAULT_INPLACE_EDIT_OPTIONS usage, if True then it use the default values not specified in your template, if False it uses these options only when the dictionnary is empty (when you do put any options in your template)
    ADAPTOR_INPLACEEDIT_EDIT = 'app_name.perms.MyAdaptorEditInline' # Explain in Permission Adaptor API
    ADAPTOR_INPLACEEDIT = {'myadaptor': 'app_name.fields.MyAdaptor'} # Explain in Adaptor API


In your urls.py
===============

::

    urlpatterns = patterns('',

        #...#

        (r'^inplaceeditform/', include('inplaceeditform.urls')),

        #...#
    )

If you use the date adaptor or datetime adaptor also:

::

    js_info_dict = {
        'packages': ('django.conf',),
    }

    urlpatterns = patterns('',

        #...#

        (r'^inplaceeditform/', include('inplaceeditform.urls')),
        (r'^jsi18n$', 'django.views.i18n.javascript_catalog', js_info_dict),
    )
